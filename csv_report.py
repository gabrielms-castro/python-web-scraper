import csv


def write_csv_report(page_data, filename="report.csv"):
    with open(filename, "w", newline="", encoding="utf-8") as file:
        fieldnames = [
            "page_url",
            "h1",
            "first_paragraph",
            "outgoing_link_urls",
            "image_urls",
        ]
        writer = csv.DictWriter(file, fieldnames)

        writer.writeheader()

        for page in page_data.values():
            row = {
                "page_url": page["url"],
                "h1": page["h1"],
                "first_paragraph": page["first_paragraph"],
                "outgoing_link_urls": ";".join(page["outgoing_links"]),
                "image_urls": ";".join(page["image_urls"]),
            }
            writer.writerow(row)
