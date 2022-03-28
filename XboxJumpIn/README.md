# Xbox Jump In
### Demo: https://themindvirus.github.io/unity-dev/XboxJumpIn/
![screenshot](https://github.com/themindvirus/unity-dev/blob/main/XboxJumpIn/XboxJi.png)
### Developer Commentary
![screenshot](https://github.com/themindvirus/unity-dev/blob/main/XboxJumpIn/XboxJiDev.png)
### Rate Limiting Errors
During development of Xbox Ji Firmware there were issues with \
GitHub Actions deploying to GitHub Pages as they performed a server migration.
![screenshot](https://github.com/themindvirus/unity-dev/blob/main/XboxJumpIn/XboxJiError.png)

An incident was reported to GitHub Status regarding "Degraded Performance" of GitHub Pages. \
Following 2 hours of downtime, service was resumed (with some logs missing from GitHub Actions). \
During the downtime, it succeeded to build but failed to deploy a simple test page: \
URL: https://github.com/themindvirus/github-pages-test \
This repository can now be used as a service availability checker for the hosting service.