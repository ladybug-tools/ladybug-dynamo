# ladybug-dynamo

Ladybug-dynamo is the ladybug plugin for Dynamo to import and visualize weather data from and EnergyPlus Weather file ([EPW](https://www.energyplus.net/sites/default/files/docs/site_v8.3.0/InputOutputReference/07-WeatherData/index.html)).

![sunlighthours analysis](https://raw.githubusercontent.com/ladybug-analysis-tools/ladybug-dynamo/master/resources/sunlighthoursAnalysis/definition.JPG)

Ladybug-dynamo is developed in IronPython and uses [Revit API](https://knowledge.autodesk.com/search-result/caas/CloudHelp/cloudhelp/2016/ENU/Revit-API/files/GUID-F0A122E0-E556-4D0D-9D0F-7E72A9315A42-htm.html) and [Dynamo libraries](https://github.com/DynamoDS) to take inputs from Revit model or create geometrical outputs. For core functionalities it uses [ladybug core libraries](https://github.com/ladybug-tools/ladybug) which is developed in Python 2.7.

## Installation
You must install [Dynamo with Revit or Dynamo Studio](http://dynamobim.org/download/) to use this plugin. The Revit specific nodes won't work in Dynamo Studio. For the plugin itself you can always download the latest stable version from [Dynamo's package manger](http://dynamopackages.com/#). Once you install it from Dynamo package manager it sould be ready to use.


## Example files and tutorials
There are [several example files](http://hydrashare.github.io/hydra/?keywords=ladybugdynamo) on Hydra to get yourself started with ladybug for Dynamo. There is a YouTube video associated with some of the examples which can also be found at [this link](https://www.youtube.com/playlist?list=PLkjfDmSc5OryQ0FD9vUVNU6dQaIM4RPDD).

![sunpath](https://raw.githubusercontent.com/ladybug-analysis-tools/ladybug-dynamo/master/resources/sunpath/sunpath.gif)

## API Documentation
Latest API documentation is available at [this page](http://ladybug-tools.github.io/ladybug-dynamo/doc/index.html). [Let us know](https://github.com/ladybug-tools/ladybug-dynamo/issues/) if you find any mistakes in the documentation.

## Road Map
- [x] First release for proof of concept.
- [ ] Second release with enhanced performance.
- [ ] Improve Revit integration (e.g. load data based on Revit location, etc.).
- [ ] Add visualization components. This is dependant on Dynamo's features for visualization 

## dependencies
[ladybug-core](https://github.com/ladybug-tools/ladybug) for all the non-geometrical calculations. ladybug-core is licensed under GPLV3.
