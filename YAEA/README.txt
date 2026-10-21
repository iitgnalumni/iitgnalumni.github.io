YOUNG ALUMNI EXCELLENCE AWARDS WEBSITE
IIT Gandhinagar, Office of Alumni Relations
==================================================

WHAT IS IN THIS FOLDER
  index.html    The complete website (one page). The IITGN logo is built in.
  photos/       Awardee photos go here.
  images/       The campus picture shown beside "Submit a Nomination".
  README.txt    This file.

FOR THE PERSON LAUNCHING THE SITE
  Upload the whole folder (index.html, photos/ and images/) to the web server, keeping
  the folder structure as it is. No database, build step or plugins are needed.
  It is a plain static page and works on any web host.

--------------------------------------------------
ADDING PHOTOS
--------------------------------------------------
1. Save each photo as a .jpg file (portrait or square, about 600 x 700 px,
   face near the top centre).
2. Name it EXACTLY as shown below (lowercase, hyphens, .jpg).
3. Put it in the "photos" folder. That's it - no code change needed.

If a photo is missing, the site shows the person's initials instead.
For 2022-2024 awardees the site shows the photo from the old Google Site
until you add a file here. Adding your own copies is recommended, because
those old links stop working if the Google Site is deleted.

  2025  parichita-kapoor.jpg
        akanksha-jagwani.jpg
        prasannajeet-mane.jpg
  2024  sumitava-mukherjee.jpg
        vishnu-kumar-gupta.jpg
        ajinkya-kulkarni.jpg
        abhik-patel.jpg
        nisarg-shah.jpg
  2023  aishwarya-agrawal.jpg
        silky-agrawal.jpg
        saurya-prakash.jpg
        prashant-borde.jpg
  2022  kislay-pankaj.jpg
        yogesh-goyal.jpg
        sarthak-jain.jpg
        prathamesh-juvatkar.jpg

Tip: on Windows, turn on "File name extensions" (View menu in File Explorer)
so a file is not accidentally saved as "name.jpg.jpg".

--------------------------------------------------
ADDING LINKEDIN PROFILES
--------------------------------------------------
Open index.html in Notepad (right-click > Open with > Notepad) and search
(Ctrl+F) for the person's name. In that line, paste the profile link between
the quotes after linkedin:

    linkedin:"https://www.linkedin.com/in/their-profile/",

Leave it as linkedin:"" to hide the LinkedIn button for that person.

--------------------------------------------------
ADDING NEXT YEAR'S AWARDEES
--------------------------------------------------
In index.html, search for "EDIT HERE EACH YEAR".
1. Copy one existing awardee entry, paste it at the top of the AWARDEES list,
   and change the year, name, slug, programme, department, graduation year,
   category, role, LinkedIn link and biography paragraphs.
     Categories: PRO = Outstanding Professional Achievement
                 ACA = Outstanding Academic Achievement
                 ENT = Outstanding Entrepreneurship
                 LSI = Excellence in Leadership, Public Influence,
                       Societal Impact & Volunteerism
2. Add a line for the new year in COHORTS (a short note about the cohort).
3. Change FEATURED_YEAR to the new year.
4. Add each new photo to the photos folder using the slug as the file name.
The awardee list, year buttons, counts and footer links update automatically.

NOMINATIONS
  In the same section, NOMINATIONS sets whether nominations are open, the
  closing date (e.g. deadline: "31 March 2027") and the Google Form link.

Contact: alumnirelations@iitgn.ac.in
