# tfs-build-alert-pi
Alert via Raspberry Pi when there is a build failure from TFS.

- Using Azure Service Bus Queue to send build status messages to and pickup via Python script.
- Python script looks for failed builds and adds to array.
- If array is empty the green light is activated.
- If array has failed build the red light is activated.
- Only one light active at a time.
