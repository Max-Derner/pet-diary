[Welcome Page](../README.md)

## *__Cost breakdown__*
__DISCLAIMER__: This breakdown is only done to the best of my abilities, I cannot guarantee any running costs at all.  

* __DynamoDB__:
    * 25 Read Capacity Units for free
    * 25 Write Capacity Units for free
    * Point In Time Recovery: $0.23772 per GB-month (can comment out in [template.yaml](../template.yaml))
* __KMS Key__: 
    * $1 per key generated (can comment out in [template.yaml](../template.yaml))
    * Gets 20,000 requests free per month
* __Lambda__:
    * 1 million free requests a month
    * Up to 3.2 million seconds of free compute time per month (37 days worth of runtime)
* __SNS__:
    * 1 million free requests a month

My personal experience so far has been costs of £1 to £1.10 a month, your mileage may vary.

