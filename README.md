# Afanasy Pools Addin <img src="https://github.com/laurence-trippen/Afanasy-Pools-Addin/blob/master/Preview/afpools2.png" align="right" width="128">
Provisionally Afanasy Pools Support. It's not the official implementation. it's more of a workaround.

With the Afanasy Pools Addin you can create pools and assign clients to them. When you create an Afanasy job, whether using the AfStarter or a software plugin, you can always specify a pool for rendering.

The pools are more a superficial solution and are not stored in the **Afanasy's code**, so you don't see any pools in the [**Afanasy Web GUI**](http://cgru.info/afanasy/gui#web) or in the [**Afanasy Qt GUI**](http://cgru.info/afanasy/gui#page_top).

## CGRU - Afanasy Render Manager

[CGRU - Afanasy Website](http://cgru.info/afanasy/afanasy)

## Afanasy Pool Manager

![](https://github.com/laurence-trippen/Afanasy-Pools-Addin/blob/master/Preview/keeperaddin.jpg?raw=true)
![](https://github.com/laurence-trippen/Afanasy-Pools-Addin/blob/master/Preview/mainview.JPG?raw=true)
![](https://github.com/laurence-trippen/Afanasy-Pools-Addin/blob/master/Preview/createpool.JPG?raw=true)
![](https://github.com/laurence-trippen/Afanasy-Pools-Addin/blob/master/Preview/deletepool.JPG?raw=true)
![](https://github.com/laurence-trippen/Afanasy-Pools-Addin/blob/master/Preview/addclients.JPG?raw=true)
![](https://github.com/laurence-trippen/Afanasy-Pools-Addin/blob/master/Preview/networkscan.JPG?raw=true)
![](https://github.com/laurence-trippen/Afanasy-Pools-Addin/blob/master/Preview/addhostname.JPG?raw=true)

## Blender Pool Integration
![](https://github.com/laurence-trippen/Afanasy-Pools-Addin/blob/master/Preview/blender-plugin-pools.jpg?raw=true)
![](https://github.com/laurence-trippen/Afanasy-Pools-Addin/blob/master/Preview/blender-plugin-select-pool.jpg?raw=true)

## History - Why this project?

On the [**CGRU Afanasy Roadmap**](http://cgru.info/roadmap) a pool support is planned for the future. But since we needed a provisional pool solution in one project, we developed one ourselves which works through a workaround.

The project still has its weaknesses in some places, because it has been developed rapidly.
If there are bugs, just create an issue on Github.

## How does it works?

![](https://github.com/laurence-trippen/Afanasy-Pools-Addin/blob/master/Preview/plan.jpg?raw=true)

# Pool emulation by hosts exclude mask.

```python
def get_excluded_hostnames(all_clients, pool_clients):
  excluded = []
  for client in all_clients:
    if not client in pool_clients:
      excluded.append(client)
  return excluded
```


