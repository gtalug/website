title: GTALUG Key Signing Party

GTALUG sometimes hosts [Key signing parties](https://en.wikipedia.org/wiki/Key_signing_party) at the regular meetings.

The next one is on:

* [9 June, 2015](http://gtalug.org/meeting/2015-06/) at 7:30 p.m.

### What you will need to do to participate

1. Create an OpenPGP keypar for yourself (if you haven't) already.
2. Add your key to the Keysigning Keyring.
    a. Export your public key `gpg --export KEYID > MyPublicKey.gpg`
    b. Get a copy of the Keysigning Keyring (send an email to the Key Master <me+gtalug@mylesbraithwaite.com>).
    c. Add your public key to the Keysigning Keyring `gpg --no-default-keyring --keyring ./keysigning-keyring --import MyPublicKey.gpg`
    d. Submit the updated keysiging keyring (e-mail it to the KeyMaster <me+gtalug@mylesbraithwaite.com>).
3. **OR** E-Mail your public key to the keymaster and let him do the work.
4. Bring a goverment-issued picture ID of yourself.

#### Help

Get your KEYID from your keyring as the part following the 1024D/ as follows:

    gpg --list-secret-keys | grep sec

Get your fingerprint information:

    gpg --fingerprint KEYID

### At the Key Signing Party

1. Each participant should meet up face to face with every other participant to receive their key fingerprint and examine their ID, and to give them your key fingerprint and have them examine your ID.
2. As you meet up with each person they will give you a printout of their key fingerprint and show you their ID. Examine their ID, and if you are convinced that the person standing in front of you is actually who they say they are then write 'ID OK' on their key fingerprint and initial it to prevent tampering. You then keep their key fingerprint in a safe place for later reference after the event has finished.

### After the Key Signing Party

1. Find the key ID on the fingerprint. The fingerprint will have an 8-character ID listed after the key size. Typically it looks like this: '1024D/64011A8B'. The actual ID portion is the '64011A8B'. You'll notice this is also the last 8 characters of the fingerprint itself.
2. Fetch the public key using the key ID. If you're running GnuPG on the command line, you can do this by typing: `gpg --keyserver pgp.mit.edu --recv-keys <KeyID>` (where KeyID is obviously the ID of the key you want).
3. Check that the fingerprint of the key you've just fetched matches the fingerprint on the slip of paper: `gpg --fingerprint <KeyID>` and compare it with the hard copy in front of you.
4. If (and only if) you are happy that the fingerprints match and the person showed you sufficient ID, you can do the actual 'signing' part of the process: `gpg --sign-key <KeyID>` and answer the questions it asks.
5. Next you need to send the signed copy of their key back to them. Now upload the signed key back to the server `gpg --keyserver pgp.mit.edu --send-key <Key_ID>`. You should get back something like 'gpg: sending key <Key_ID> to hkp server pgp.mit.edu'.
