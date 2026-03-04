#!/usr/bin/env python3
"""
AUREON BROWSER - Selenium-based web control
No coordinates needed - finds elements by text/name like a human!
"""

from typing import Dict, Any, Optional
import time

try:
    from selenium import webdriver
    from selenium.webdriver.common.by import By
    from selenium.webdriver.common.keys import Keys
    from selenium.webdriver.support.ui import WebDriverWait
    from selenium.webdriver.support import expected_conditions as EC
    from selenium.webdriver.chrome.service import Service as ChromeService
    from selenium.webdriver.edge.service import Service as EdgeService
    SELENIUM_AVAILABLE = True
except ImportError:
    SELENIUM_AVAILABLE = False


class AureonBrowser:
    """
    Browser control using Selenium - finds elements by text, no coordinates!
    """
    
    def __init__(self):
        if not SELENIUM_AVAILABLE:
            raise RuntimeError("Selenium not installed: pip install selenium")
        
        self.driver = None
        self._connect_to_existing_browser()
    
    def _connect_to_existing_browser(self):
        """Connect to user's existing browser session"""
        # Try Chrome first
        try:
            options = webdriver.ChromeOptions()
            options.add_experimental_option("debuggerAddress", "127.0.0.1:9222")
            self.driver = webdriver.Chrome(options=options)
            print("[OK] Connected to Chrome browser")
            return
        except Exception:
            pass
        
        # Try Edge
        try:
            options = webdriver.EdgeOptions()
            options.add_experimental_option("debuggerAddress", "127.0.0.1:9222")
            self.driver = webdriver.Edge(options=options)
            print("[OK] Connected to Edge browser")
            return
        except Exception:
            pass
        
        print("[WARN]?  Could not connect to existing browser")
        print("    Start Chrome/Edge with: --remote-debugging-port=9222")
    
    def click_element_by_text(self, text: str) -> Dict[str, Any]:
        """Click on any element containing this text"""
        if not self.driver:
            return {"ok": False, "error": "browser_not_connected"}
        
        try:
            # Try multiple strategies
            selectors = [
                f"//button[contains(text(), '{text}')]",
                f"//a[contains(text(), '{text}')]",
                f"//*[contains(text(), '{text}')]",
                f"//input[@value='{text}']",
            ]
            
            for selector in selectors:
                try:
                    element = self.driver.find_element(By.XPATH, selector)
                    element.click()
                    return {
                        "ok": True,
                        "text": text,
                        "output": f"clicked '{text}'"
                    }
                except Exception:
                    continue
            
            return {"ok": False, "error": f"element '{text}' not found"}
            
        except Exception as e:
            return {"ok": False, "error": repr(e)}
    
    def type_text(self, text: str, clear_first: bool = False) -> Dict[str, Any]:
        """Type text into the active element"""
        if not self.driver:
            return {"ok": False, "error": "browser_not_connected"}
        
        try:
            active = self.driver.switch_to.active_element
            if clear_first:
                active.clear()
            active.send_keys(text)
            
            return {
                "ok": True,
                "text": text,
                "output": f"typed {len(text)} characters"
            }
        except Exception as e:
            return {"ok": False, "error": repr(e)}
    
    def press_key(self, key: str) -> Dict[str, Any]:
        """Press a key (enter, tab, escape, etc)"""
        if not self.driver:
            return {"ok": False, "error": "browser_not_connected"}
        
        try:
            key_map = {
                "enter": Keys.ENTER,
                "tab": Keys.TAB,
                "escape": Keys.ESCAPE,
                "backspace": Keys.BACKSPACE,
                "delete": Keys.DELETE,
            }
            
            key_obj = key_map.get(key.lower(), key)
            active = self.driver.switch_to.active_element
            active.send_keys(key_obj)
            
            return {"ok": True, "key": key, "output": f"pressed {key}"}
        except Exception as e:
            return {"ok": False, "error": repr(e)}
    
    def go_to_url(self, url: str) -> Dict[str, Any]:
        """Navigate to URL"""
        if not self.driver:
            return {"ok": False, "error": "browser_not_connected"}
        
        try:
            if not url.startswith("http"):
                url = "https://" + url
            
            self.driver.get(url)
            time.sleep(1)  # Wait for page load
            
            return {
                "ok": True,
                "url": url,
                "output": f"navigated to {url}"
            }
        except Exception as e:
            return {"ok": False, "error": repr(e)}
    
    def switch_to_tab(self, title_contains: str) -> Dict[str, Any]:
        """Switch to tab by title"""
        if not self.driver:
            return {"ok": False, "error": "browser_not_connected"}
        
        try:
            original_window = self.driver.current_window_handle
            
            for window in self.driver.window_handles:
                self.driver.switch_to.window(window)
                if title_contains.lower() in self.driver.title.lower():
                    return {
                        "ok": True,
                        "title": self.driver.title,
                        "output": f"switched to '{self.driver.title}'"
                    }
            
            self.driver.switch_to.window(original_window)
            return {"ok": False, "error": f"no tab with '{title_contains}' found"}
            
        except Exception as e:
            return {"ok": False, "error": repr(e)}
    
    def new_tab(self, url: Optional[str] = None) -> Dict[str, Any]:
        """Open new tab"""
        if not self.driver:
            return {"ok": False, "error": "browser_not_connected"}
        
        try:
            self.driver.execute_script("window.open('');")
            self.driver.switch_to.window(self.driver.window_handles[-1])
            
            if url:
                return self.go_to_url(url)
            
            return {"ok": True, "output": "opened new tab"}
        except Exception as e:
            return {"ok": False, "error": repr(e)}
    
    def scroll(self, direction: str = "down", amount: int = 300) -> Dict[str, Any]:
        """Scroll page"""
        if not self.driver:
            return {"ok": False, "error": "browser_not_connected"}
        
        try:
            scroll_amount = amount if direction == "down" else -amount
            self.driver.execute_script(f"window.scrollBy(0, {scroll_amount});")
            
            return {"ok": True, "output": f"scrolled {direction} {amount}px"}
        except Exception as e:
            return {"ok": False, "error": repr(e)}
