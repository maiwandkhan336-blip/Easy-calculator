[app]

title = EasyCalculator
package.name = easycalculator
package.domain = org.maiwand

source.dir = .
source.include_exts = py,png,jpg,kv,json

version = 1.0

requirements = python3,kivy

orientation = portrait
fullscreen = 0

android.permissions =

android.api = 36
android.minapi = 23

android.archs = arm64-v8a, armeabi-v7a

android.private_storage = True

android.presplash_color = #ffffff

warn_on_root = 0


[buildozer]

log_level = 2
warn_on_root = 0