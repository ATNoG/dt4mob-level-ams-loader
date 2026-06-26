# Level AMS Loader - User Manual

## Overview

Level AMS Loader is a data synchronization service for geotechnical monitoring systems. It extracts data from the Level AMS API and loads it into Eclipse Ditto via Eclipse Hono, enabling digital twin capabilities for geotechnical assets and their instruments.

**Problem it solves:** Geotechnical monitoring generates continuous data from instruments like inclinometers and load cells. This service keeps the digital twin platform (Eclipse Ditto) synchronized with the latest asset configurations and measurement values, while optionally maintaining historical records through a dedicated history API.

**Primary use case:** Designed to run as a Kubernetes CronJob for automated periodic synchronization. Also supports manual execution for initial data loads or historical data recovery.
