def get_order_info(soup):
    order_names = [
        "Order No:",
        "Order placed at:",
        "Order delivered at:",
        "Order Status"
    ]

    order_info = {}

    for order_name in order_names:
        order_b_tag = soup.select_one(f'td > p:-soup-contains("{order_name}") > b')
        order_strong_tag = soup.select_one(f'td > p:-soup-contains("{order_name}") > strong')

        if order_b_tag:
            order_info[order_name] = order_b_tag.text.strip()
        elif order_strong_tag:
            order_info[order_name] = order_strong_tag.text.strip()
        else:
            
            order_info[order_name] = "Not Found"

    return order_info

def get_restaurant_info(soup):
    ordered_from_name = "Ordered from:"

    ordered_from_h5_tag = soup.select_one(f'td:-soup-contains("{ordered_from_name}") h5 > strong')
    ordered_from_b_tag = soup.select_one(f'td:-soup-contains("{ordered_from_name}") h5 > b')

    restaurant_name = "Not Found"
    restaurant_address = "Not Found"

    if ordered_from_h5_tag:
        restaurant_name = ordered_from_h5_tag.text.strip()
        next_p_tag = ordered_from_h5_tag.find_next('p')
        if next_p_tag:
            restaurant_address = next_p_tag.text.strip()

    elif ordered_from_b_tag:
        restaurant_name = ordered_from_b_tag.text.strip()
        next_p_tag = ordered_from_b_tag.find_next('p')
        if next_p_tag:
            restaurant_address = next_p_tag.text.strip()

    return {'restaurant_name':restaurant_name, 'restaurant_address': restaurant_address}


def get_customer_info(soup):
    delivery_label = "Delivery To:"
    customer_name_tag = soup.select_one(f'td:-soup-contains("{delivery_label}") > p:nth-of-type(2)')
    customer_address_tags = soup.select(f'td:-soup-contains("{delivery_label}") > h5')


    customer_name = "Not Found"
    customer_address = "Not Found"

    if customer_name_tag:
        customer_name = customer_name_tag.text.strip()

    if customer_address_tags:
        customer_address = " ".join(tag.text.strip() for tag in customer_address_tags)

    return {"customer_name" : customer_name, "customer_address" : customer_address}



def extract_item_details(soup):
    item_details = []

    # Find all rows with meaningful data
    rows = soup.select('tbody tr:has(td:nth-of-type(3))')

    for row in rows:
        # Extract the cells in each row
        cells = row.find_all('td')

        # Check if all cells contain non-empty text
        if all(cell.text.strip() for cell in cells):
            item_name = cells[0].text.strip()
            quantity = int(cells[1].text.strip())
            price = cells[2].text.strip()

            price = float(price.replace('₹', '').replace(',', '').replace('-', '').replace('₹\xa0', '').strip()) if price else 0.0
      
            item_details.append((item_name, quantity, price))

    return item_details


def extract_order_summary(soup):
    summary_details = {
        'Platform fee': 0.0,  # Set platform fee to 0 by default
    }

    # Find all rows with summary details
    rows = soup.select('tbody tr')

    for row in rows:
        # Check for summary items
        try:
            if 'Item Total' in row.text:
                value = row.find_all('td')[-1].text.strip().replace('₹', '').replace(',', '').replace('-', '').replace('₹\xa0', '').strip()
                summary_details['Item Total'] = float(value) if value else 0.0
            elif 'Order Packing Charges' in row.text:
                value = row.find_all('td')[-1].text.strip().replace('₹', '').replace(',', '').replace('-', '').replace('₹\xa0', '').strip()
                summary_details['Order Packing Charges'] = float(value) if value else 0.0
            elif 'Delivery partner fee' in row.text:
                value = row.find_all('td')[-1].text.strip().replace('₹', '').replace(',', '').replace('-', '').replace('₹\xa0', '').strip()
                summary_details['Delivery partner fee'] = float(value) if value else 0.0
            elif 'Discount Applied' in row.text:
                value = row.find_all('td')[-1].text.strip().replace('₹', '').replace(',', '').replace('-', '').replace('₹\xa0', '').strip()
                summary_details['Discount Applied'] = -float(value) if value else 0.0
            elif 'Taxes' in row.text:
                value = row.find_all('td')[-1].text.strip().replace('₹', '').replace(',', '').replace('-', '').replace('₹\xa0', '').strip()
                summary_details['Taxes'] = float(value) if value else 0.0
            elif 'Platform fee' in row.text:
                value = row.find_all('td')[-1].text.strip().replace('₹', '').replace(',', '').replace('-', '').replace('₹\xa0', '').strip()
                summary_details['Platform fee'] = float(value) if value else 0.0  
            elif 'Order Total' in row.text:
                value = row.find_all('td')[-1].text.strip().replace('₹', '').replace(',', '').replace('-', '').replace('₹\xa0', '').strip()
                summary_details['Order Total'] = float(value) if value else 0.0
        except:
            pass

    return summary_details

