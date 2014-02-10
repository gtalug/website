title: GTALUG Key Signing Party

GTALUG sometimes hosts [Key signing parties](https://en.wikipedia.org/wiki/Key_signing_party) at the regular meetings.

The next one is on:

* [11 Feburary, 2014](http://gtalug.org/meeting/2014-02/) at 7:30 p.m.

### What you will need:

1. Create an OpenPGP keypair for yourself (if you haven't) already.
2. Print or write down your key fingerprint and bring it with you. You'll have to confirm at the signing that the list is correct for your key.
3. Send you key before the event to the `pgp.mit.edu` keyserver.
4. Email your key fingerprint to <me+gtalug-keys@mylesbraithwaite.com> with the subject `'me@example.org' key` (of course replacing 'me@example.org' with your actually email address).
5. Bring a goverment-issued picture ID of yourself.

#### Help

Get your KEYID from your keyring as the part following the 1024D/ as follows:

    gpg --list-secret-keys | grep sec

Here is how to send your public key to the keyserver:

    gpg --keyserver gpg.mit.edu --send-keys <KEYID>

Get your fingerprint information:

    gpg --fingerprint KEYID

### At the Key Signing Party

1. Each participant should meet up face to face with every other participant to receive their key fingerprint and examine their ID, and to give them your key fingerprint and have them examine your ID.
2. Each participant should meet up face to face with every other participant to receive their key fingerprint and examine their ID, and to give them your key fingerprint and have them examine your ID.

### After the Key Signing Party

1. Find the key ID on the fingerprint. The fingerprint will have an 8-character ID listed after the key size. Typically it looks like this: '1024D/64011A8B'. The actual ID portion is the '64011A8B'. You'll notice this is also the last 8 characters of the fingerprint itself.
2. Fetch the public key using the key ID. If you're running GnuPG on the command line, you can do this by typing: `gpg --keyserver pgp.mit.edu --recv-keys <KeyID>` (where KeyID is obviously the ID of the key you want).
3. Check that the fingerprint of the key you've just fetched matches the fingerprint on the slip of paper: `gpg --fingerprint <KeyID>` and compare it with the hard copy in front of you.
4. If (and only if) you are happy that the fingerprints match and the person showed you sufficient ID, you can do the actual 'signing' part of the process: `gpg --sign-key <KeyID>` and answer the questions it asks.
5. Next you need to send the signed copy of their key back to them. Now upload the signed key back to the server `gpg --keyserver pgp.mit.edu --send-key <Key_ID>`. You should get back something like 'gpg: sending key <Key_ID> to hkp server pgp.mit.edu'.
