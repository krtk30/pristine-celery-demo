# HR App Documentation

This document describes the **Employee ↔ Department** app in the `pristine` project.

## Contents

1. [Overview](#overview)  
2. [Models](#models)  
3. [API Endpoints](#api-endpoints)  
4. [Signals & Logging](#signals--logging)  
5. [Setup & Running](#setup--running)  

---

## Overview

The HR app manages employees and their department memberships.  
It exposes a REST API for CRUD operations and logs every M2M change via a `m2m_changed` signal into `logs/hr.log`.

---