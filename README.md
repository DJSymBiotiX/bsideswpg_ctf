BSides Winnipeg CTF
=============

My solutions to the CTF contest for BSides Winnipeg
https://ctf.bsideswpg.ca

yo
--
As with a few other people, I apparently put too much thought into the solution for this first challenge.
I opened it up in vim and noticed that it was an x86\_64 linux binary, so I instinctively threw it on one
of my linux boxes and ran it there.

When I ran it:

\# ./yo

I was greeted with "Yo, gimme something!", which led me to assume it was looking for some input.

\# ./yo something

"Dawg, you're \*lame\*!". I figured I was getting somewhere, so I kept giving it input.

After 2 argments, all it ever returns is "Yo, you're deluging me!". I decided to look up the word "deluging"
which means "flooding" or something like that, which led me to believe this was some sort of buffer overflow.
After trying to give it obscenely large arguments with no success, I decided to open it up in vim again.
I realized that the passwords (since they are being submitted as http urls) had to be continuous (containing underscores).
I found the correct string symbol in the binary, and thus completed the challenge.

A friend of mine who had already solved this challenge then showed me the "strings" command, which possibly could have
saved me a lot of time.

oldschool
---------
This challenge is actually quite easy, yet slightly time consuming.

You are presented this image:
<img src="https://ctf.bsideswpg.ca/challs/oldschool.png" style="height: 30%; width: 30%;" />

At first, I thought there was some sort of pattern to it.
"If the top hole is punched, it looks like 0 is not punched", etc.
I decided to give up and work on a few other challenges at this point as I could not figure out the pattern to this weird
looking card. A little while later a light went off in my head "Aha! It's a punch card!".

I looked up punch card on google and stumbled upon this image in the punch card wiki:
<img src="http://upload.wikimedia.org/wikipedia/commons/4/4c/Blue-punch-card-front-horiz.png" style="height: 40%; width: 40%" />

This punchcard is the lookup key for punch cards of this style. Using the key and the original punch card, all you must do at this point
is figure out which letters/symbols correspond to each column of punches, and the password is yours.

pitch
-----
With this challenge, you are supplied a tar file "pitch.tar".

At first I opened it with vim as vim can show you the contents of compressed packages.
I noticed 2 files with the same name, but initially thought nothing of it.
If you untar the file "tar xvf pitch.tar", the result is just one file "pitch/cast5.gpg.gz". Looking at this file gave me no clues to what
the password was. 

I then remembered the other file I saw when I opened it in vim. I decided to open it once again in vim to open the other file that
was not extracted. Within that file was the password in plain text. Done.

tootsie
-------
Once again, you are presented a tar file, this one being quite big. 

Initial instinct was to open it in vim. Another tar file you say? Odd.

Going further, I noticed that each compressed package contained another compressed package, of a different format no less (zip, rar, tar, bz2, 7z, etc) starting at number 998 and continuously going down.
"tootsie", the name of the challenge, explained to me the nature of this tar file. 

"How many licks does it take to get to the center of a tootsie pop".

I then realized that this was going to be a straight up extraction problem, I decided to write a script to extract the sequential files using the proper program
based on the file type. My solution can be found in this github project as "tootsie.sh". Once you get to "the center", you find the password.

tapdat
------
Another image puzzle. [It's a little too wide to show here directly]

https://ctf.bsideswpg.ca/challs/tapdat.png

Being familiar with Linear Feedback Shift Registers from my university days, I already knew what had to be done here.
You "tap" into the bits on the far right that have the lines connected to them and apply the circuit logic to them, you then prepend
the result to the beginning of the big sequence, as every other bit shifts one to the right.

First off, I decided to figure out which bit corresponded to which segment as I just figured that it wouldnt be a standard configuration (and I was right!).
I didn't know how many time I would need to pull this shift off, so instead of drawing the segments out by hand I decided to write a python script to do it for me.

This script can be found in this repo as "tapdat.py" along with a file called "binary" which was all the bits from the image put into a file for the script.
In any case, it turns out you only need to shift it once and you are presented with the password in a seven segment display kind of way which I will paste here cause of the tricky "W"

     _       _           _               _                   _           _           _   _   _       _
    |_|     |_| |   | | |_      |     | | | | | |    _|     |_  |_| |   |_  |_      |_| |   |_| |   | |
    | |. _  |   |_  |_|  _|  _  |_| |_| |_| |_| |_  |_|  _   _| | | |   |   |_   _  | | |_| | | |   | |

As it turns out, the problem in itself was incorrect. The image shows XNOR gates, but it should be showing XOR gates.
With XNOR gates, it outputs a 1 as the first bit (which creates that A. character), but it should actually be a 0 as the dot is not part of the solution.

dangle
------
This challenge was actually really easy for me as I work with git every day.

You are presented with a tar file once again, but looking into it you realize it contains a git project.
Initially I took a look at the git log, and went back to the very first commit to see if I could find anything there.
Nothing of interest there, so I decided to dive into the .git folder and snoop around in there. Noticed there was something in the "lost-found" folder,
and lo and behold, there was the password.

I suppose you could call that one a hunch.

factoryfresh
------------
This challenge seemed to be where the difficulty really picked up. 

You are given a pcap file (which is a dump of a packet capture using a program such as wireshark for example).
I checked it out using tcp dump, and didn't really get anywhere so I decided to install wireshark and start poking around with it in there.
Opening it up in wireshark, I found a few things of interest. It was a dump of an SSL/TLS http exchange, so it was encrypted. I also noticed some strings in the dump that proved
to be valuable. It looked like this was run through a fresh dd-wrt install. 

I assumed that dd-wrt had to have some sort of default ssl key installed that was public knowledge so I began
scrounging the web for the private key. With no luck in sight, I was directed to something called "little black box". Little Black Box is a program somebody made which contains
a plethora of default private keys for a bunch of different hardware. Inputting the pcap file into this little black box returns a private key. Then, putting this private key into wireshark
for this pcap dump allows it to unencrypt the data, and voila, there is the password.

cryptic
-------
Ah yes, more encryption problems.
You are given a shell script with the following line:

"openssl enc -e -aes-128-ofb -K $encryption\_key -iv 0000000000000000 < "$1" > "$1".enc"

You are also given "message1", "message1.enc", "message2", "message2.enc" and "flag.enc".

The assumption here is that the line in the shell script was used to create the enc versions of the message files, as well as the flag file.
The thing to note here was the algorithm used: "-aes-128-ofb". I assumed there was some sort of known plaintext attack on this cipher as you are given
the plaintext as well as the encrypted text for message 1 and 2. Looking online, I found the diagram for this particular cipher and some example code
for how to generate the keystream from a known plaintext/known ciphertext point of view.

My python solution lies in cryptic.py. The script uses the first 2 arguments: the plaintext, and the ciphertext, to generate the keystream used to encrypt the data.
The second part of the script uses the generated keystream to unencrypt the third argument "flag.enc", which results in the password for the challenge.

p.s. I'll give credit to the python script I found online that helped me solve this: https://gist.github.com/craSH/2969666
With a little more time I probably could have derived this algorithm to pull out the keystream myself, but meh that's what the internet is for :P

rascal
------
Finally, a programming challenge.

You are given a haskell program that takes in an argument, does a bunch of stuff to it (more on that later), and checks the result against a known
answer in the program itself. Your job is to figure out what the "bunch of stuff" is doing and reverse it.
Seeing as I knew *nothing* about haskell, I had to approach this slowly. I edited the haskell program to apply the algorithm one piece at a time
to figure out what each command was doing.

Basically, it takes input, converts the chars to their integer representation, and reverses them.
Then for each integer (x), if it's even it will print out x^3,x^2 else it will print out x,x^2.
Then it will interleave the results into 2 arrays, and put that into an array itself.
You are then left with an array of 2 arrays.

Once you know what is happening, the solution is pretty simple (my python solution can be found in rascal.py).
Thus, you reverse the known answer, and you are left with the password.

demo
----
This one was pretty tricky (unless you know the easy way to do it).

You are given "demo.img". Right off the bat, I notice that this is some sort of image file (duh) so initially I tried mounting it but ran into problems
as it wasnt working. After a bit of trouble not being able to figure out what to do, I used the "file" command to see if it could give me more insight as
to what file format this actually was. 

"COM executable for DOS".

Aha, it's a DOS program. I remembered back to the first challenge, and hoped that the answer was just a symbol in the image file, so I used objdump on demo.img to try and find any symbols, or maybe to understand the assembly code. No dice.
My next thought was "hmm, this is a DOS program, maybe DOSBox or some other DOS emulator can run it". Threw dosbox on my linux box and tried to run it,
only to be returned with a bunch of crazy garbled coloured text (guess this doesn't work so well in a shell). 

After a bunch of attempts, and a few different DOS emulators, I was reminded by a friend that virtualbox can emulate dos. After dicking around with virtual box for a bit, I eventually realized that this
img file was an image of a floppy disk. I created a new DOS emulation in virtual box and set the img file to its virtual A drive, and voila, a crazy
dos program with the password being outputted.

asshat
------
Another image challenge.

You are given the following image:
<img src="https://ctf.bsideswpg.ca/challs/asshat.jpg" style="width: 20%; height: 50%" />

First clue seemed obvious. Figure out what colour #DABCB4 is. I opened up the inspector, and changed the colour of the background to the color noted
on the card (figured this was the best place to do it, since I could have the image reference right beside it).

The colour turns out to be the same colour as the finger nails in the image which led me to "thumbnail".

I went to http://regex.info/exif.cgi and loaded the image into the program. After it processes the image, you are told that the thumbnail for the
image is actually different from the image itself. Clicking on the thumbnail and zooming in (since it's so small) you notice a bunch of dots and
dashes on the bottom of the image. 

This stumped me for a bit until an onlooking friend pointed out that the dots and dashes appeared to be morse code.
That was exactly what it was. Translating the morse code into text revealed the password.

bootliquor, cosmo, scumbag
--------------------------
The last three challenged I didn't really even attempt. Bootliquor was another .img challenge, cosmos was a really weird image challenge (a picture of a shoe),
and I was told that scumbag was just ridiculously evil (which it turns out was correct).


The End
=======
