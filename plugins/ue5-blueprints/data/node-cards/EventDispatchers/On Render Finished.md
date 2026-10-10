## On Render Finished
**Category:** EventDispatchers
**Search:** "On Render Finished"

**Description:** Assign a function to this delegate to get notified when each individual job is finished. THIS WILL ONLY BE CALLED IF USING THE RENDERJOB CONVENIENCE FUNCTION. Because there can only be one job in the queue when using RenderJob, this will be called when the render is complete, and the executor has been released. This allows you to queue up another job immediately as a result of the OnRenderFinished callback.
---
