from selenium import webdriver
from webdriver_manager.chrome import ChromeDriverManager

def loadTime(url):
    # Using Chrome as driver of websites
    driver = webdriver.Chrome(ChromeDriverManager().install())
    #driver=webdriver.Chrome('/Users/asmaahakami/Documents/chromedriver')
    # Get the url of website by driver
    driver.get(url)
    
    # Compute load time
    load_time = driver.execute_script(
            """
            var loadTime = ((window.performance.timing.domComplete - window.performance.timing.navigationStart)/1000);
            return loadTime;
            """
            )
    return load_time


