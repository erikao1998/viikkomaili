## Overview

This script is used to send a mail that contains upcoming events of a student organization. Usually it is done manually but I decided to automatize it because it is a quite boring yet important task that must be done weekly.

## How it works

First the script uses Selenium to copy the content of the mail from our web page. After that it edits the data by formatting the text and removing some events if needed. Finally the mail is sent by using Python library "smtplib" and *voilà*, the message is sent.
