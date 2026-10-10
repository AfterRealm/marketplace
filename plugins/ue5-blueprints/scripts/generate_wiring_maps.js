#!/usr/bin/env node
// generate_wiring_maps.js — Parse UE5 Blueprint T3D exports into compact wiring maps
//
// Usage: node generate_wiring_maps.js [--input DIR] [--output DIR]
//   --input   Directory containing .t3d files (default: current dir)
//   --output  Directory for wiring maps (default: ./wiring_maps)
//
// Processes ALL .t3d files in the input directory.
// Output: one .md wiring map per Blueprint graph function.

const fs = require('fs');
const path = require('path');

// Parse CLI args
const args = process.argv.slice(2);
let inputDir = '.';
let outputDir = './wiring_maps';

for (let i = 0; i < args.length; i++) {
  if (args[i] === '--input' && args[i + 1]) inputDir = args[++i];
  if (args[i] === '--output' && args[i + 1]) outputDir = args[++i];
}

inputDir = path.resolve(inputDir);
outputDir = path.resolve(outputDir);

// Friendly names for common node classes
const CLASS_LABELS = {
  'K2Node_FunctionEntry': 'Entry',
  'K2Node_FunctionResult': 'Return',
  'K2Node_CallFunction': 'Call',
  'K2Node_CallParentFunction': 'Parent',
  'K2Node_IfThenElse': 'Branch',
  'K2Node_Knot': 'Reroute',
  'K2Node_VariableGet': 'Get',
  'K2Node_VariableSet': 'Set',
  'K2Node_CallArrayFunction': 'ArrayOp',
  'K2Node_BreakStruct': 'BreakStruct',
  'K2Node_MakeStruct': 'MakeStruct',
  'K2Node_PromotableOperator': 'MathOp',
  'K2Node_MacroInstance': 'Macro',
  'K2Node_CommutativeAssociativeBinaryOperator': 'MathOp',
  'K2Node_Self': 'Self',
  'K2Node_DynamicCast': 'Cast',
  'K2Node_GetArrayItem': 'ArrayGet',
  'K2Node_ExecutionSequence': 'Sequence',
  'K2Node_SwitchInteger': 'SwitchInt',
  'K2Node_SwitchString': 'SwitchString',
  'K2Node_SwitchName': 'SwitchName',
  'K2Node_SwitchEnum': 'SwitchEnum',
  'K2Node_Select': 'Select',
  'K2Node_TemporaryVariable': 'TempVar',
  'K2Node_AssignmentStatement': 'Assign',
  'K2Node_CreateWidget': 'CreateWidget',
  'K2Node_GetDataTableRow': 'GetDataTableRow',
  'K2Node_AddComponentByClass': 'AddComponent',
  'K2Node_Event': 'Event',
  'K2Node_CustomEvent': 'CustomEvent',
  'K2Node_AssignDelegate': 'AssignDelegate',
  'K2Node_CallDelegate': 'CallDelegate',
  'K2Node_ComponentBoundEvent': 'ComponentEvent',
  'K2Node_AddComponent': 'AddComponent',
  'K2Node_SpawnActor': 'SpawnActor',
  'K2Node_SpawnActorFromClass': 'SpawnActor',
  'K2Node_Timeline': 'Timeline',
  'K2Node_Tunnel': 'Tunnel',
  'K2Node_ForEachElementInEnum': 'ForEachEnum',
  'EdGraphNode_Comment': 'Comment',
};

function splitIntoGraphs(content) {
  const graphs = {};
  const lines = content.split('\n');
  const knownGraphs = new Set();
  for (const line of lines) {
    const trimmed = line.trim();
    const declMatch = trimmed.match(/Begin Object Class=\/Script\/Engine\.EdGraph\s+Name="([^"]+)"/);
    if (declMatch) knownGraphs.add(declMatch[1]);
  }

  let currentGraph = null;
  let depth = 0;
  let graphLines = [];

  for (const line of lines) {
    const trimmed = line.trim();
    let graphName = null;
    const graphMatchFull = trimmed.match(/Begin Object Class=\/Script\/Engine\.EdGraph\s+Name="([^"]+)"/);
    if (graphMatchFull) {
      graphName = graphMatchFull[1];
    } else {
      const graphMatchShort = trimmed.match(/^Begin Object Name="([^"]+)"/);
      if (graphMatchShort && knownGraphs.has(graphMatchShort[1])) {
        graphName = graphMatchShort[1];
      }
    }

    if (graphName) {
      currentGraph = graphName;
      depth = 1;
      graphLines = [line];
      continue;
    }

    if (currentGraph) {
      graphLines.push(line);
      if (trimmed.startsWith('Begin Object')) depth++;
      if (trimmed === 'End Object') {
        depth--;
        if (depth === 0) {
          if (!graphs[currentGraph] || graphLines.length > graphs[currentGraph].split('\n').length) {
            graphs[currentGraph] = graphLines.join('\n');
          }
          currentGraph = null;
          graphLines = [];
        }
      }
    }
  }
  return graphs;
}

function buildClassLookup(content) {
  const classLookup = {};
  const lines = content.split('\n');
  for (const line of lines) {
    const trimmed = line.trim();
    const declMatch = trimmed.match(/^Begin Object Class=\/Script\/\w+\.(\w+)\s+Name="([^"]+)"/);
    if (declMatch) classLookup[declMatch[2]] = declMatch[1];
  }
  return classLookup;
}

function parsePin(pinData) {
  const get = (key) => {
    const re = new RegExp(key + '=([^,)]+)');
    const m = pinData.match(re);
    return m ? m[1] : null;
  };
  const getQuoted = (key) => {
    const re = new RegExp(key + '="([^"]*)"');
    const m = pinData.match(re);
    return m ? m[1] : null;
  };

  const pinId = get('PinId');
  const pinName = getQuoted('PinName') || get('PinName');
  const direction = getQuoted('Direction');
  const category = getQuoted('PinType.PinCategory');
  const defaultVal = getQuoted('DefaultValue') || get('DefaultValue');
  const hidden = get('bHidden');

  const linkedToMatch = pinData.match(/LinkedTo=\(([^)]*)\)/);
  const linkedTo = [];
  if (linkedToMatch && linkedToMatch[1]) {
    const entries = linkedToMatch[1].split(',').filter(s => s.trim());
    for (const entry of entries) {
      const parts = entry.trim().split(' ');
      if (parts.length >= 2) linkedTo.push({ nodeName: parts[0], pinId: parts[1] });
    }
  }

  const friendlyMatch = pinData.match(/PinFriendlyName=NSLOCTEXT\("[^"]*",\s*"([^"]*)"/);
  const friendlyName = friendlyMatch ? friendlyMatch[1] : null;
  const subObjMatch = pinData.match(/PinType\.PinSubCategoryObject="?([^",)]+)/);
  const subObj = subObjMatch ? subObjMatch[1] : null;
  const isRef = get('PinType.bIsReference') === 'True';

  return {
    id: pinId, name: pinName, friendlyName,
    direction: direction === 'EGPD_Output' ? 'out' : 'in',
    category, isRef, defaultValue: defaultVal,
    linkedTo, hidden: hidden === 'True', subObj,
  };
}

function parseGraphSection(content, globalClassLookup) {
  const lines = content.split('\n');
  const nodes = [];
  const nodesByName = {};
  let currentNode = null;
  let nodeDepth = 0;

  for (const line of lines) {
    const trimmed = line.trim();
    const beginMatchFull = trimmed.match(/^Begin Object Class=\/Script\/\w+\.(\w+)\s+Name="([^"]+)"/);
    const beginMatchShort = !beginMatchFull ? trimmed.match(/^Begin Object Name="([^"]+)"/) : null;

    let cls = null, nodeName = null;
    if (beginMatchFull) { cls = beginMatchFull[1]; nodeName = beginMatchFull[2]; }
    else if (beginMatchShort) { nodeName = beginMatchShort[1]; cls = globalClassLookup[nodeName]; }

    if (cls && nodeName && !cls.startsWith('EdGraph_') && cls !== 'EdGraph') {
      if (currentNode) { nodeDepth++; continue; }
      currentNode = {
        name: nodeName, class: cls, shortClass: cls,
        label: CLASS_LABELS[cls] || cls,
        funcRef: null, opName: null, varRef: null, structType: null,
        macroRef: null, widgetClass: null, dataTableRef: null,
        castClass: null, eventRef: null, delegateRef: null,
        posX: 0, posY: 0, pins: [], comment: null,
      };
      nodeDepth = 1;
      continue;
    }

    if (trimmed.startsWith('Begin Object') && currentNode) { nodeDepth++; continue; }
    if (trimmed === 'End Object') {
      if (currentNode) {
        nodeDepth--;
        if (nodeDepth === 0) {
          if (nodesByName[currentNode.name]) {
            const oldIdx = nodes.indexOf(nodesByName[currentNode.name]);
            if (oldIdx !== -1) nodes.splice(oldIdx, 1);
          }
          nodesByName[currentNode.name] = currentNode;
          nodes.push(currentNode);
          currentNode = null;
        }
      }
      continue;
    }

    if (!currentNode || nodeDepth > 1) continue;

    const funcMatch = trimmed.match(/FunctionReference=\(.*?MemberName="([^"]+)"/);
    if (funcMatch) currentNode.funcRef = funcMatch[1];
    const opMatch = trimmed.match(/OperationName="([^"]+)"/);
    if (opMatch) currentNode.opName = opMatch[1];
    const varMatch = trimmed.match(/VariableReference=\(.*?MemberName="([^"]+)"/);
    if (varMatch) currentNode.varRef = varMatch[1];
    const structMatch = trimmed.match(/StructType=.*?ScriptStruct'[^']*\.(\w+)'/);
    if (structMatch) currentNode.structType = structMatch[1];
    const macroMatch = trimmed.match(/MacroGraphReference=.*?MacroGraph=.*?Name="([^"]+)"/);
    if (macroMatch) currentNode.macroRef = macroMatch[1];
    const widgetMatch = trimmed.match(/WidgetType=.*?Class'[^']*\.(\w+)'/);
    if (widgetMatch) currentNode.widgetClass = widgetMatch[1];
    const dtMatch = trimmed.match(/DataTable=.*?DataTable'[^']*\/(\w+)\.\w+'/);
    if (dtMatch) currentNode.dataTableRef = dtMatch[1];
    const castMatch = trimmed.match(/TargetType=.*?Class'[^']*\.(\w+)'/);
    if (castMatch) currentNode.castClass = castMatch[1];
    const eventMatch = trimmed.match(/EventReference=\(.*?MemberName="([^"]+)"/);
    if (eventMatch) currentNode.eventRef = eventMatch[1];
    const delegateMatch = trimmed.match(/DelegatePropertyName="([^"]+)"/);
    if (delegateMatch) currentNode.delegateRef = delegateMatch[1];
    const customFuncMatch = trimmed.match(/^CustomFunctionName="([^"]+)"/);
    if (customFuncMatch) currentNode.funcRef = currentNode.funcRef || customFuncMatch[1];
    const posXMatch = trimmed.match(/^NodePosX=(-?\d+)/);
    if (posXMatch) currentNode.posX = parseInt(posXMatch[1]);
    const posYMatch = trimmed.match(/^NodePosY=(-?\d+)/);
    if (posYMatch) currentNode.posY = parseInt(posYMatch[1]);
    const commentMatch = trimmed.match(/^NodeComment="([^"]+)"/);
    if (commentMatch) currentNode.comment = commentMatch[1].trim();
    if (trimmed.startsWith('CustomProperties Pin (')) {
      const pinData = trimmed.slice('CustomProperties Pin ('.length, -1);
      const pin = parsePin(pinData);
      if (pin) currentNode.pins.push(pin);
    }
  }
  return nodes;
}

function buildPinLookup(nodes) {
  const lookup = {};
  const byPinIdOnly = {};
  for (const node of nodes) {
    for (const pin of node.pins) {
      lookup[`${node.name} ${pin.id}`] = { nodeName: node.name, pinName: pin.name, pin };
      if (!byPinIdOnly[pin.id]) byPinIdOnly[pin.id] = [];
      byPinIdOnly[pin.id].push({ nodeName: node.name, pinName: pin.name, pin });
    }
  }
  lookup._resolve = function(targetNodeName, targetPinId) {
    const exact = lookup[`${targetNodeName} ${targetPinId}`];
    if (exact) return exact;
    const candidates = byPinIdOnly[targetPinId];
    if (candidates && candidates.length === 1) return candidates[0];
    if (candidates) {
      const match = candidates.find(c => c.nodeName === targetNodeName);
      if (match) return match;
      return candidates[0];
    }
    return undefined;
  };
  return lookup;
}

function shortNodeName(node) {
  if (node.label === 'Reroute') return `Reroute_${node.name.split('_').pop()}`;
  if (node.label === 'Comment') return `Comment`;
  if (node.widgetClass) return `CreateWidget(${node.widgetClass})`;
  if (node.dataTableRef) return `GetDataTableRow(${node.dataTableRef})`;
  if (node.castClass) return `Cast(${node.castClass})`;
  if (node.macroRef) return `Macro(${node.macroRef})`;
  if (node.eventRef) return `Event(${node.eventRef})`;
  if (node.delegateRef) return `Delegate(${node.delegateRef})`;
  if (node.varRef) return `${node.label}(${node.varRef})`;
  if (node.funcRef) return node.funcRef + (node.name.match(/_(\d+)$/) ? `_${node.name.match(/_(\d+)$/)[1]}` : '');
  if (node.opName) return node.opName;
  if (node.structType) return `${node.label}(${node.structType})`;
  return node.label || node.name;
}

function generateWiringMap(graphName, nodes, pinLookup) {
  const lines = [];
  const timestamp = new Date().toISOString().slice(0, 19).replace('T', ' ');

  lines.push(`# ${graphName} -- Wiring Map`);
  lines.push(`# Generated: ${timestamp}`);
  lines.push(`# Source: T3D export (${nodes.length} nodes)`);
  lines.push('');

  const codeNodes = nodes.filter(n => n.shortClass !== 'EdGraphNode_Comment');
  const comments = nodes.filter(n => n.shortClass === 'EdGraphNode_Comment');
  codeNodes.sort((a, b) => a.posX - b.posX || a.posY - b.posY);

  // Node Inventory
  lines.push('## Nodes');
  for (let i = 0; i < codeNodes.length; i++) {
    lines.push(`  [${i + 1}] ${shortNodeName(codeNodes[i])}  (${codeNodes[i].name})`);
  }
  lines.push('');

  // Execution Flow
  lines.push('## Execution Flow');
  for (const node of codeNodes) {
    const sn = shortNodeName(node);
    for (const pin of node.pins) {
      if (pin.category !== 'exec' || pin.direction !== 'out' || pin.linkedTo.length === 0) continue;
      for (const link of pin.linkedTo) {
        const target = pinLookup._resolve(link.nodeName, link.pinId);
        if (!target) continue;
        const targetNode = codeNodes.find(n => n.name === target.nodeName);
        if (!targetNode) continue;
        const pinLabel = pin.name === 'then' ? '' : `.${pin.friendlyName || pin.name}`;
        lines.push(`  ${sn}${pinLabel} -> ${shortNodeName(targetNode)}`);
      }
    }
  }
  lines.push('');

  // Data Wiring
  lines.push('## Data Wiring');
  for (const node of codeNodes) {
    const sn = shortNodeName(node);
    for (const pin of node.pins) {
      if (pin.category === 'exec' || pin.hidden || pin.direction !== 'out' || pin.linkedTo.length === 0) continue;
      for (const link of pin.linkedTo) {
        const target = pinLookup._resolve(link.nodeName, link.pinId);
        if (!target) continue;
        const targetNode = codeNodes.find(n => n.name === target.nodeName);
        if (!targetNode) continue;
        let annotation = '';
        if (node.shortClass === 'K2Node_BreakStruct') annotation = '  [COPY from BreakStruct]';
        if (target.pin && target.pin.isRef) annotation += '  [by-ref]';
        lines.push(`  ${sn}.${pin.name} -> ${shortNodeName(targetNode)}.${target.pinName}${annotation}`);
      }
    }
  }
  lines.push('');

  // Default Values
  const defaults = [];
  for (const node of codeNodes) {
    const sn = shortNodeName(node);
    for (const pin of node.pins) {
      if (pin.hidden || pin.linkedTo.length > 0) continue;
      if (!pin.defaultValue || pin.defaultValue === 'None' || pin.defaultValue === '') continue;
      if (pin.name === 'self') continue;
      defaults.push(`  ${sn}.${pin.name} = ${pin.defaultValue}`);
    }
  }
  if (defaults.length > 0) {
    lines.push('## Default Values');
    lines.push(...defaults);
    lines.push('');
  }

  // Variables
  const vars = new Set();
  for (const node of codeNodes) {
    if (node.varRef) {
      const mode = node.shortClass.includes('Set') ? 'Set' : 'Get';
      vars.add(`  ${node.varRef} (${mode})`);
    }
  }
  if (vars.size > 0) {
    lines.push('## Variables');
    lines.push(...[...vars].sort());
    lines.push('');
  }

  // Comments
  if (comments.length > 0) {
    lines.push('## Comments');
    for (const c of comments) {
      if (c.comment) lines.push(`  "${c.comment.replace(/\s+/g, ' ').trim()}"`);
    }
    lines.push('');
  }

  return lines.join('\n');
}

// --- Main ---
function main() {
  if (!fs.existsSync(inputDir)) {
    console.error(`Input directory not found: ${inputDir}`);
    process.exit(1);
  }

  if (!fs.existsSync(outputDir)) fs.mkdirSync(outputDir, { recursive: true });

  // Find all .t3d files in input dir
  const t3dFiles = fs.readdirSync(inputDir).filter(f => f.endsWith('.t3d'));
  if (t3dFiles.length === 0) {
    console.log(`No .t3d files found in ${inputDir}`);
    console.log('Run blueprint-export first to generate T3D files.');
    process.exit(0);
  }

  console.log(`Processing ${t3dFiles.length} T3D file(s) from ${inputDir}`);
  let totalGenerated = 0;

  for (const file of t3dFiles) {
    const filePath = path.join(inputDir, file);
    console.log(`\nProcessing: ${file}`);

    let content = fs.readFileSync(filePath, 'utf-8');
    content = content.replace(/\0/g, ''); // Strip null bytes from UTF-16LE exports

    const globalClassLookup = buildClassLookup(content);
    const graphs = splitIntoGraphs(content);
    const graphNames = Object.keys(graphs);
    console.log(`  Found ${graphNames.length} graphs: ${graphNames.join(', ')}`);

    for (const graphName of graphNames) {
      // Skip internal graphs
      if (graphName.endsWith('_MERGED') || graphName.startsWith('EdGraph_') || graphName.startsWith('ExecuteUbergraph_')) {
        continue;
      }

      const nodes = parseGraphSection(graphs[graphName], globalClassLookup);
      if (nodes.length === 0) {
        console.log(`  ${graphName}: 0 nodes, skipping`);
        continue;
      }

      const pinLookup = buildPinLookup(nodes);
      const wiringMap = generateWiringMap(graphName, nodes, pinLookup);
      const outPath = path.join(outputDir, `${graphName}.md`);
      fs.writeFileSync(outPath, wiringMap, 'utf-8');

      console.log(`  ${graphName}: ${nodes.length} nodes -> ${graphName}.md`);
      totalGenerated++;
    }
  }

  console.log(`\nDone — ${totalGenerated} wiring maps generated in ${outputDir}`);
}

main();
