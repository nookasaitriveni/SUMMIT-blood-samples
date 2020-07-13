
def get_page_numbers(current_page, number_of_pages, extremes=2, arounds=3):
    """
    Get "digg-style" page numbers

    i.e. show first, last and adjacent page numbers with those in between
    collapsed / omitted.

    :param current_page:
        Current page number, 1-based integer
    :param number_of_pages:
        Total number of pages
    :param extremes:
        Number of extreme page numbers (first/last) to display
    :param arounds:
        Number of page numbers to display on each side of the current page

    :returns:
        list of page numbers to display, with None as placeholder for those
        which were collapsed
    """
    threshold = (2*extremes) + (2*arounds) + 1
    all_page_numbers = range(1, number_of_pages+1)

    if number_of_pages > threshold:
        first = all_page_numbers[:extremes]
        last = all_page_numbers[-extremes:]
        idx = current_page - 1
        around = all_page_numbers[max(idx-arounds, 0):idx+arounds+1]

        pages_to_show = sorted(set().union(first, around, last))
        page_numbers = [pages_to_show[0]]
        for i, page_number in enumerate(pages_to_show[1:], 1):
            last_page = pages_to_show[i-1]
            if page_number - last_page == 2:
                page_numbers.append(page_number-1)
            elif page_number - last_page > 1:
                page_numbers.append(None)
            page_numbers.append(page_number)
        return page_numbers
    else:
        return all_page_numbers
