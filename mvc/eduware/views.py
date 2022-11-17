from contextlib import _RedirectStream
from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
import random
from datetime import date


