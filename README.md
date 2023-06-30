# SwiggyOrdersData

This script extracts all Swiggy Orders data into a CSV including Order ID, Order Details, Payment Method, Amount and Restaurant information.

# How to use

The script expects you to give your Swiggy session as input.

- Login to swiggy.com on a browser (chrome or firefox)
- Install the [Cookie Editor chrome extension](https://chrome.google.com/webstore/detail/cookie-editor/hlkenndednhfkekhgcdicdfddnkalmdm?hl=en) or the [Cookie Editor firefox extension](https://addons.mozilla.org/en-US/firefox/addon/cookie-editor/)
- Go to the Swiggy tab and click on the Extension's icon, and select "Export". This will copy your cookies to clipboard
- Create a new file called `cookies.json` in the same directory as the `GenerateData.py` script and paste the copied cookies into this file.
- Install requirements with `pip`
  ```
  pip install -r requirements.txt
  ```
- Now simply run `GenerateData.py` to get swiggy orders data

  ```
  python swiggy.py
  ```

