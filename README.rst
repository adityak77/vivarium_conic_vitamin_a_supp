===============================
vivarium_conic_vitamin_a_supp
===============================

Research repository for work on vitamin A supplementation for the purposes of the
Conic grant. The work is being done by Aditya Kannan during July and August of 2019. 
The scope is to complete a vitamin A supplementation model that includes cost
estimation. Vitamin A fortifcation will be included if time permits.

.. contents::
   :depth: 1

Model Overiew
-------------

A general outline of the model is described below. More detailed information
should be contained in a concept model document which is yet to be created for
this project.

Population, Causes and Risks
~~~~~~~~~~~~~~~~~~~~~~~~~~~~

This vitamin A model considers the risk factor of vitamin A deficiency as well
as a gap in coverage (we call this a risk factor as well), the lack of vitamin A
supplementation. It considers the diseases of Measles, diarrheal diseases, and
lower respiratory infections among those aged zero to five years old.

Roughly, the diseases impact mortality and morbidity in the population. The
risk factor vitamin A deficiency impacts the incidence rate of each of these
diseases. The coverage gap impacts the exposure to vitamin A deficiency itself.
The coverage gap is dichotomous, and can be interpreted as "being supplemented"
or not.

Intervention
~~~~~~~~~~~~

The Supplementation intervention is implemented as a "magic wand" that shifts
exposure to the coverage gap, i.e. lack of vitamin A supplementation, to a new
value. It does this by calculating an annual step size linearly from the start
and end years of the simulation and shifting the exposure down on-demand using
the value system.

This vitamine A supplementation is the explicit goal of this work, but
fortification remains a stretch goal and thus a possibility.

Installation
------------

These models require data from GBD databases. You'll need several internal
IHME packages and access to the IHME cluster.

To install the extra dependencies create a file called ~/.pip/pip.conf which
looks like this::

    [global]
    extra-index-url = http://pypi.services.ihme.washington.edu/simple
    trusted-host = pypi.services.ihme.washington.edu


To set up a new research environment, open up a terminal on the cluster and
run::

    $> conda create --name=vivarium_conic_vitamin_a_supp python=3.6
    ...standard conda install stuff...
    $> conda activate vivarium_conic_vitamin_a_supp
    (vivarium_conic_vitamin_a_supp) $> conda install redis
    (vivarium_conic_vitamin_a_supp) $> git clone git@github.com:ihmeuw/vivarium_conic_vitamin_a_supp.git
    ...you may need to do username/password stuff here...
    (vivarium_conic_vitamin_a_supp) $> cd vivarium_conic_vitamin_a_supp
    (vivarium_conic_vitamin_a_supp) $> pip install -e .


Usage
-----

You'll find four directories inside the main
``src/vivarium_conic_vitamin_a_supp`` package directory:

- ``components``

  This directory is for Python modules containing custom components for
  the vivarium_conic_vitamin_a_supp project. You should work with the
  engineering staff to help scope out what you need and get them built.

- ``external_data``

  If you have **small scale** external data for use in your sim or in your
  results processing, it can live here. This is almost certainly not the right
  place for data, so make sure there's not a better place to put it first.

- ``model_specifications``

  This directory should hold all model specifications and branch files
  associated with the project.

- ``verification_and_validation``

  Any post-processing and analysis code or notebooks you write should be
  stored in this directory.

