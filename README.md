Playwright tests

This project is focused on implementing basic testing of given links:
https://vuejs.org/examples/#form-bindings
https://vuejs.org/examples/#modal
https://vuejs.org/examples/#crud

It is divided into three python files, where each file is testing one of the pages. 
For testing is used pytest and playwright. 
For starting the tests of scripts can be used:
pytest
If you would like to also check how it looks like in the browser use:
pytest --headed
If it is neede to have it in more slowmotion use(in ms):
pytest --headed --slowmo 1000 

