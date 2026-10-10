## Set Root Proxy Component Space Transform
**Category:** Physics
**Search:** "Set Root Proxy Component Space Transform"
**Target:** Geometry Collection Component

**Inputs:**
- In (exec)
- Target (object)
- Index (integer)
- Root Proxy Transform (transform)

**Outputs:**
- Out (exec)

**Description:** blueprint function to set a specific root proxy local transform warning: when called from C++ and calling it on multiple root proxies it is recommended to use SetRootProxyLocalTransform instead and then call RefreshCustomRenderer to avoid the cost of refreshing the renderer each time
---
