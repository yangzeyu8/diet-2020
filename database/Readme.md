The recipe data is scraped from https://www.allrecipes.com/ and USDA.

You can download it here https://drive.google.com/file/d/1H64ykNL71GfG6mPyRsvPy0DIGvnjQjJV/view?usp=sharing. 

Need the following packages:
```python
import pandas as pd
import json
import time
import os
from urllib.request import urlopen
from bs4 import BeautifulSoup
import re
```

To run the web scraper program:

```python
cd allrecipes-web-scraper
python main.py
```

