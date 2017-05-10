# AWSPricer - A Pricing API for AWS
#### Currently Supports EC2

---

**Description:**
This is a pricing API for AWS. This currently supports EC2. I have created 
filters for products that can be built on top of each other to get backs lists
that can then be priced and returned.

**Example:**

```
pricer = awspricer('us-east-1')
for price in pricer.getproductsbyos('Linux',pricer.getproductsbyregion('us-east-1')):
        print(price['attributes']['operatingSystem'])
        print(price['attributes']['location'])
```

The above will get products by OS and then region

You can then return the filter sets to pricing and get back prices.



