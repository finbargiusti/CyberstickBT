# Cyberstick
Cyberstick is a unique file-sharing system. The coding is complex but the user interface is simple. It works like a USB stick. If you have a USB stick you can put files on it and give it to a friend so that they can access them. Cyberstick is just like that, except it is online.
Cyberstick shares some features Dropbox or Google Drive as files can be shared (although that is not the main function of Dropbox or Google Drive, which are a type of cloud storage).
Cyberstick is different because:

1. You do not have provide personal data such as your name/ email address.
2. Users are completely anonymous. Nobody can trace a single session back to any particular
user.
3. No login.

Cyberstick can be displayed on any device and still be user-friendly. There is a beta version [here](http://cyberstick.click).
In the upload section there is a drag-and- drop box or, for non drag-and- drop compatible devices, you can click and add files to the upload box. The ID for the file is displayed and there is a download link, i.e.:

cyberstick.click/download/[ID]

Now you can send the link/ID to the recipient.
The link will be automatically deleted in exactly 15 minutes (under consideration).
The IDs are in the format of three easy to remember capitalised words pulled from an [online dictionary](https://svnweb.freebsd.org/csrg/share/dict/words?view=co).
Because Cyberstick has open source API (Application Programming Interface) that has been published by me (and is free to use and republish), developers can build apps that use Cyberstick in the background serve as a portal to my service.
There is an online tutorial on the Help page of the website
Cyberstick offers a secure file-sharing system that cannot be definitively traced to them. Their data cannot. Moreover there is NO FOOTPRINT on the internet of the file ever having existed in the first place. The person who purchases the session is in theory traceable but it can never be proven that they ever shared a file.
For example:

* Lawyers would find Cyberstick useful because they would be able to exchange sensitive
material with their colleagues.
* Inventors would find it useful if they were moving around non-patented information.
* If Hillary Clinton had been using Cyberstick she would never have had any problems with her
email being hacked.

Currently the payment method involves payment with your credit card at a rate of 1 cent per session (i.e. per single file shared). I am planning to add some other forms of payment, such as Bitcoin (100% anonymous) and other systems.
The language for the webframe is Python. For web handling, I use a library known as Python-Flask that uses the libraries Werkzeug and Jinja 2. A “library” is a file that you can import that gives you many different functions. A “function” in programming is an algorithm that can be called upon with different parameters and it runs on based on what you have entered.
All of the programming used in Cyberstick is completely unique. I wrote it all myself.
