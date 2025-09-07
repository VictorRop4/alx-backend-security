# Security API

This project is a Django REST Framework-based API for monitoring and managing request logs, blocked IPs, and suspicious IP addresses. It includes **token-based authentication** and **Swagger UI documentation** for easy testing.

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

---

## Features

- Log all incoming requests (`RequestLog`).  
- Block and unblock IP addresses (`BlockedIP`).  
- Track suspicious IPs with reasons and timestamps (`SuspiciousIP`).  
- Token-based authentication for secure API access.  
- Rate-limited simulated login endpoint.  
- Swagger UI integration with global token authorization.  

---

## Requirements

- Python 3.12+  
- Django 4.x  
- Django REST Framework  
- Django REST Framework Authtoken  
- drf-yasg (Swagger)  
- django-ratelimit  

Install Python packages:

```bash
pip install -r requirements.txt
