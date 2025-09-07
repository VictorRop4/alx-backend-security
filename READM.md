# Security API

A Django REST Framework API for monitoring and managing **request logs**, **blocked IPs**, and **suspicious IP addresses**.  
This API is secured using **Token Authentication** and includes **Swagger UI** for interactive documentation and testing.

---

## Table of Contents

- [Features](#features)  
- [Requirements](#requirements)  
- [Installation](#installation)  
- [Environment Variables](#environment-variables)  
- [Database Setup](#database-setup)  
- [Token Authentication](#token-authentication)  
- [API Endpoints](#api-endpoints)  
- [Swagger UI](#swagger-ui)  
- [Usage](#usage)  
- [License](#license)  

---

## Features

- Log incoming requests (`RequestLog`).  
- Block and unblock IP addresses (`BlockedIP`).  
- Track suspicious IPs with reasons and timestamps (`SuspiciousIP`).  
- Token-based authentication for secure API access.  
- Rate-limited simulated login endpoint.  
- Swagger UI integration for easy testing with token authorization.  

---

## Requirements

- Python 3.12+  
- Django 4.x  
- Django REST Framework  
- Django REST Framework Authtoken  
- drf-yasg (Swagger)  
- django-ratelimit  

Install dependencies:

```bash
pip install -r requirements.txt
