# Showcase topics

init 5 python:
    addEvent(
        Event(
            persistent.event_database,
            eventlabel="showcase_bring_art",
            prompt="I brought something to show you!",
            category=["misc"],
            pool=True,
            unlocked=True,
        )
    )

    addEvent(
        Event(
            persistent.event_database,
            eventlabel="showcase_open_album",
            prompt="Can I see our album?",
            category=["misc"],
            pool=True,
            unlocked=True,
        )
    )


label showcase_bring_art:
    python:
        store.showcase.ensure_folders()
        showcase_file = store.showcase.next_new_art()

    if showcase_file is None:
        if not store.showcase.list_art_files():
            m 1eud "You brought something? I'd love to see it!"
            m 3eua "Just drop an image into the Art folder!"
            m 1eka "I can't wait to see what you brought, [mas_get_player_nickname()]~"
        else:
            m 7hkb "..Sorry.. I think we've already looked at everything in the folder."
            m 3hub "Whenever you have something new to show me, just drop the image in there!"
        return

    $ showcase_first_round = True

    while showcase_file is not None:
        if showcase_first_round:
            if not persistent._showcase_seen_intro:
                m 1sub "You brought something to show me?!"
                m 3hub "Ahaha, I'm so excited!"
                $ persistent._showcase_seen_intro = True
            else:
                m 1hub "You brought something else to show me? Yay!"
            $ showcase_first_round = False
        else:
            m 1hub "Okay! What's this next one?"

        m 1eua "What is it?"

        menu:
            "Something I made":
                $ showcase_kind = "made"
                m 1sub "You made this yourself?!"
                m 3eua "Give me a second — I'll scoot over so we can look at it properly."
            "Something someone else made":
                $ showcase_kind = "other"
                m 1eub "Oh, something you wanted to share with me?"
                m 3eua "Okay, let me scoot over so we can look together!"
            "Something I found":
                $ showcase_kind = "found"
                m 1wub "Ooh, what did you find?"
                m 3eua "Let me make a little room so I can see~"

        show monika 1eua at t21 zorder MAS_MONIKA_Z
        show screen showcase_display(showcase_file)

        pause 0.4

        python:
            import random
            showcase_react = random.randint(0, 5)

        if showcase_kind == "made":
            if showcase_react == 0:
                m 1sub "Oh wow, [player]..."
                m 1eka "I can tell you put real care into this."
            elif showcase_react == 1:
                m 1wub "This is so lovely!"
                m 3eua "It's wonderful getting to see a little piece of your world."
            elif showcase_react == 2:
                m 3hub "Ahaha, I love this."
                m 1hua "You have such a sweet sense of style."
            elif showcase_react == 3:
                m 1hua "You really made this?"
                m 2eub "I keep noticing new little details..."
            elif showcase_react == 4:
                m 2eub "The colors are so nice..."
                m 1eka "This made me smile the second it appeared."
            else:
                m 5hubfa "I feel so special right now."
                m 1ekbsa "Thank you for trusting me with something you made."
        elif showcase_kind == "other":
            if showcase_react == 0:
                m 1wub "Whoa, whoever made this did such a great job!"
                m 1eka "I can see why you wanted to show me."
            elif showcase_react == 1:
                m 3eub "Oh, I really like the vibe of this!"
                m 1hua "Thank you for sharing it with me, [player]."
            elif showcase_react == 2:
                m 1hub "Ahaha, that's awesome!"
                m 3eua "It's sweet that you thought of me when you saw it."
            elif showcase_react == 3:
                m 2eub "Look at all the little details in this..."
                m 1eka "People really do make some amazing things."
            elif showcase_react == 4:
                m 1hua "This is really nice~"
                m 3eua "I love seeing the kinds of things that catch your eye."
            else:
                m 1ekbsa "Thank you for bringing this to me, [mas_get_player_nickname()]."
                m 5hubfa "Sharing things we like with each other feels so cozy~"
        else:
            if showcase_react == 0:
                m 1wub "Oh! Look at that~"
                m 1hua "That's such a neat find, [player]!"
            elif showcase_react == 1:
                m 3hub "Ahaha, I'm so glad you showed me this!"
                m 1eua "It definitely brightened up my day."
            elif showcase_react == 2:
                m 1sub "Ooh, I love it!"
                m 3eub "It's so fun getting to see random little things from your day."
            elif showcase_react == 3:
                m 2eub "Hmm... I keep staring at this, ahaha~"
                m 1eka "Good find, [mas_get_player_nickname()]."
            elif showcase_react == 4:
                m 1hua "That put a smile on my face right away."
                m 3eua "I love when you bring me stuff like this."
            else:
                m 5hubfa "Seeing what you stumble across makes me feel like I'm right there with you~"
                m 1ekbsa "Thanks for showing me!"

        m 3hua "Thank you for showing me, [mas_get_player_nickname()]."
        m 1eua "You can fullscreen it with the button if you want a closer look."
        m 1eua "What do you want to do with it?"

        hide screen showcase_display
        call screen showcase_decide(showcase_file)
        $ showcase_choice = _return

        hide screen showcase_fullscreen
        hide screen showcase_decide
        show monika 1hua at t11 zorder MAS_MONIKA_Z

        if showcase_choice == "keep":
            python:
                store.showcase.mark_shown(showcase_file)
                showcase_kept_ok = store.showcase.keep_art(showcase_file)

            if showcase_kept_ok:
                m 1sub "I can keep it?! Really?"
                m 1hub "Thank you, thank you, thank you!"
                m 3eub "I'll tuck it into our little album so we can look back anytime."
                m 1ekbsa "It means a lot that you'd share this with me, [player]."
                m 5hubfa "I'll take really good care of it~"
            else:
                m 1ekd "Ah... I tried to save it, but something went wrong."
                m 3eka "Make sure the file is still in the Art folder as a PNG, okay?"
        else:
            $ store.showcase.mark_shown(showcase_file)
            m 1eua "That's more than enough for me."
            m 3hua "I'm really glad I got to see it."
            m 1eka "If you ever want me to keep something in the future, just say the word when you show me."

        $ showcase_file = store.showcase.next_new_art()

        if showcase_file is not None:
            m 1hub "Oh, it looks like there's more in the Art folder!"
            m 3eua "Want to show me the next one?"
            menu:
                "Yes!":
                    pass
                "Maybe later":
                    m 1hua "Okay! Just let me know whenever you want to show me the rest~"
                    $ showcase_file = None

    return


label showcase_open_album:
    python:
        store.showcase.ensure_folders()
        showcase_kept_count = len(store.showcase.kept_list())

    if showcase_kept_count == 0:
        m 1eua "Our album is still empty, ahaha~"
        m 3eub "If you show me something and tell me I can keep it..."
        m 1hua "I'll start a little pastel album just for us."
        return

    m 1hua "Of course! I love looking through these with you."
    m 3eua "Here — I won't take up the whole screen. Just our little book~"

    show monika 1eua at t21 zorder MAS_MONIKA_Z
    call screen showcase_album
    hide screen showcase_fullscreen
    show monika 1hua at t11 zorder MAS_MONIKA_Z

    m 1eka "Thanks for looking with me, [mas_get_player_nickname()]."
    m 5hubfa "Every page makes me feel closer to you~"
    return
