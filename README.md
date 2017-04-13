# shakala

##### shakala —— A tiny batch multi-ports scanner base on nmap
				__              __              __
			   [  |            [  |  _         [  |
		 .--.   | |--.   ,--.   | | / ]  ,--.   | |  ,--.
		( (`\]  | .-. | `'_\ :  | '' <  `'_\ :  | | `'_\ :
		 `'.'.  | | | | // | |, | |`\ \ // | |, | | // | |,
		[\__) )[___]|__]'-;__/[__|  \_]'-;__/[___]'-;__/

##### Email: LandGrey@qq.com
-

## start:
```
git clone https://www.github.com/landgrey/shakala.git
cd shakala/
chmod 755 shakala.py
python shakala.py
```

## process:
```
[1] scan
   specify targets
   specify ports
   specify target extend mode
   specify scan threads
   wait for scan over
[2] handle
   filter target from results based on port or service
   finish or analyse scan metadata
```

## usage:
```
python shakala.py -t www.example.com
python3 shakala.py -t /domains.txt -p /ports.txt -e 5 --threads 80
python3 shakala.py -t http://victim.com/p?=1,192.168.20-60 -e 30 -p 80,81,8080,8090,8000-8100

python shakala.py -s /shakala/outputs/results_xxx.txt http
python shakala.py -s /shakala/outputs/results_xxx.txt 8080
```
