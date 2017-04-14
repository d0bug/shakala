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

## features
```
1.  provide over 300 common pentest ports, and keep update
2.  accurate and fast scan call nmap
3.  provide scan metadata and results analyse
4.  friendly input targets and ports and results output
5.  compatible both python 2.x and 3.x
```

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
[2] analyse
   filter target from results based on port or service
   finish or single analyse scan metadata if the program stops halfway, than select results
```

## usage:
```
python shakala.py -t www.example.com
python3 shakala.py -t /domains.txt -p /ports.txt -e 5 --threads 80
python3 shakala.py -t http://victim.com/p?=1,192.168.20-60 -e 30 -p 80,81,8080,8090,8000-8100

python shakala.py -s /shakala/outputs/results_xxx.txt http
python shakala.py -s /shakala/outputs/results_xxx.txt 8080
```
