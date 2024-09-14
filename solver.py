def bypass(self):
    try:
        while self.conn.page.locator("div#tiktok-verify-ele"):
            if not self.conn.page.locator("div#tiktok-verify-ele").is_visible(timeout=15000): return False
            try:
                debuglogs.info("Find background captcha")
                background_image = self.conn.page.locator("img#captcha-verify-image").get_attribute("src")
                debuglogs.info("Find slide captcha")
                slide_image = self.conn.page.locator("img.captcha_verify_img_slide").get_attribute("src")
                path_1 = "slide_background.jpeg"
                path_2 = "slide_item.png"
                debuglogs.info("Download background captcha")
                urlretrieve(background_image, path_1)
                debuglogs.info("Download slide captcha")
                urlretrieve(slide_image, path_2)
                debuglogs.info("Detect image captcha")
                image = cv2.imread(path_1)
                image = cv2.resize(image, (340,212))
                gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
                template = cv2.imread(path_2, cv2.IMREAD_GRAYSCALE)
                template = cv2.resize(template, (66,66))
                result = cv2.matchTemplate(gray, template, cv2.TM_CCOEFF_NORMED)
                min_val, max_val, min_loc, max_loc = cv2.minMaxLoc(result)
                solution = min_loc[0]
                sl_1 = (solution / 5) * 4
                sl_2 = solution - sl_1 + 4
                slide_image_item = self.conn.page.locator("img.captcha_verify_img_slide").bounding_box()
                center_x = slide_image_item['x'] + slide_image_item['width'] / 2
                center_y = slide_image_item['y'] + slide_image_item['height'] / 2
                p1 = center_x + sl_1
                p2 = p1 + sl_2
                p3 = p2 - 4
                debuglogs.info("Move slide captcha")
                self.conn.page.mouse.move(center_x, center_y)
                self.conn.page.mouse.down()
                time.sleep(0.1)
                self.conn.page.mouse.move(p1, center_y)
                time.sleep(0.2)
                self.conn.page.mouse.move(p2, center_y)
                time.sleep(0.2)
                self.conn.page.mouse.move(p3, center_y)
                time.sleep(0.2)
                self.conn.page.mouse.up()
                break
            except: pass
        return True
    except: pass
    return False