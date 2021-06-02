def extract_nums(text):
    for item in text.split(' '):
        try:
            yield float(item)
        except ValueError:
            pass
msg = "38.00 15.20   5.5      4.3     2"
a= list(extract_nums(msg))
b=a[0]
print b