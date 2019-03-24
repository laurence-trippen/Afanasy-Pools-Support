# Afanasy Pools Addin <img src="https://github.com/laurence-trippen/Afanasy-Pools-Addin/blob/master/Preview/afpools2.png" align="right" width="128">
A provisionally pools implementation for the open-source render manager [CGRU](http://cgru.info/).<br/>
It's not the official implementation. It's more of a workaround.

With the **Afanasy Pools Addin** you can create pools and assign clients to them.<br/>
When you create an Afanasy job, whether using the [AfStarter](http://cgru.info/afstarter) or a [software plugin](http://cgru.info/software/blender), you can<br/> always specify a pool for rendering.

The pools are more a superficial solution and are not stored in the **Afanasy's code**, so you don't<br/> see any pools in the [Afanasy Web GUI](http://cgru.info/afanasy/gui#web) or in the [Afanasy Qt GUI](http://cgru.info/afanasy/gui#page_top).

## Why this project?

On the [CGRU Roadmap](http://cgru.info/roadmap) a pool support is planned for the future.<br/> But since we needed a provisional pool solution in one project, we developed<br/> one ourselves which works through a workaround.

The project still has its weaknesses in some places, because it has been developed rapidly.<br/>
If there are bugs, just create an [issue on Github](https://github.com/laurence-trippen/Afanasy-Pools-Addin/issues).

## How does it works?
The implementation consists of three important components:

#### 1. MongoDB database
All pools and their associated clients are stored in the MongoDB database.

#### 2. Afanasy Pool Manager
With the Afanasy Pool Manager you can create, edit and delete pools in the MongoDB database.
Clients can also be added to or removed from these pools.

#### 3. Pool selection at job submssion
In CGRU, render jobs can be sent to the server in various ways.
Until now it is planned that pools can be specified in the [AfStarter](http://cgru.info/afstarter) and [Blender plugin](http://cgru.info/software/blender).
These plugins and programs also access the MongoDB database.

### Structure as Schema

![](https://github.com/laurence-trippen/Afanasy-Pools-Addin/blob/master/Preview/plan.jpg?raw=true)

### Pool emulation by hosts exclude mask.

For every Afanasy render job you can specify a hosts exclude mask.
In this mask individual render clients can be excluded from a job by a [regular expression](https://en.wikipedia.org/wiki/Regular_expression).

Let's assume we have a render farm with five render clients.
```
pc-01, pc-02, pc-03, pc-04 and pc-05
```
With this regular expression, we can, for example, exclude these three render clients from a job.
```Regular Expression
pc-01|pc-02|pc-04
```
This means that the job is executed on the two render clients **pc-03** and **pc-05**.

The hosts exclude mask can be used to create pools indirectly.
For example, let's take the five render clients from above.
Let's define a pool where **pc-01** and **pc-03** are contained.

From this pool the following mask would have to be generated, so that on the
Render Farm, the job can only be executed with **pc-01** and **pc-03**.

Generated mask to run job on renderfarm with **pc-01** and **pc-03**:
```Regular Expression
pc-02|pc-04|pc-05
```

This simple algorithm is used to generate an excluded client list from the included pool clients.
```python
def get_excluded_hostnames(all_renderfarm_hostnames, pool_hostnames):
  excluded_hostnames = []
  for hostname in all_renderfarm_hostnames:
    if not hostname in pool_hostnames:
      excluded_hostnames.append(hostname)
  return excluded_hostnames
```

## Features & Future plans

* [x] Pool Manager is startable from Keeper.
* [x] Create, Edit, Delete pools.
* [x] Add/Remove clients to pools.
* [x] Add online and offline afanasy clients to pool.
* [x] Network scan
* [x] PyMongo installation script for afanasy's embedded Python.
* [x] Blender plugin pool integration.
* [ ] AfStarter pool integration.
* [ ] Offline PyMongo installation for Blender and Afanasy.
* [ ] Easy installation

## Installation

Coming soon.

## Showcase

### Start Afanasy Pool Manager from Keeper

![](https://github.com/laurence-trippen/Afanasy-Pools-Addin/blob/master/Preview/keeperaddin.jpg?raw=true)

### Afanasy Pool Manager

![](https://github.com/laurence-trippen/Afanasy-Pools-Addin/blob/master/Preview/mainview.JPG?raw=true)
![](https://github.com/laurence-trippen/Afanasy-Pools-Addin/blob/master/Preview/createpool.JPG?raw=true)
![](https://github.com/laurence-trippen/Afanasy-Pools-Addin/blob/master/Preview/deletepool.JPG?raw=true)
![](https://github.com/laurence-trippen/Afanasy-Pools-Addin/blob/master/Preview/addclients.JPG?raw=true)
![](https://github.com/laurence-trippen/Afanasy-Pools-Addin/blob/master/Preview/networkscan.JPG?raw=true)
![](https://github.com/laurence-trippen/Afanasy-Pools-Addin/blob/master/Preview/addhostname.JPG?raw=true)

### Blender Pool Integration
![](https://github.com/laurence-trippen/Afanasy-Pools-Addin/blob/master/Preview/blender-plugin-pools.jpg?raw=true)
![](https://github.com/laurence-trippen/Afanasy-Pools-Addin/blob/master/Preview/blender-plugin-select-pool.jpg?raw=true)
