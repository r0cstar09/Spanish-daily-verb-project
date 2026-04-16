"""
Polysemous Spanish verbs (English prompts do not map to one gloss — like 'get').

Each bank: 6 senses × 20 lines = 120, with rotating grammar `lesson` tags via polysemous_helpers.
Extend POLYSEMOUS_BUILDERS in polysemous_content.py with POLYSEMOUS_BUILDERS_EXT.
"""

from __future__ import annotations

from typing import Callable

from polysemous_helpers import build_multisense_from_specs


def _bank(sense_templates: dict[str, tuple[str, ...]]) -> list[dict]:
    """Exactly six senses, 20 lines each; each value is a tuple of format strings (use {i} where useful)."""
    if len(sense_templates) != 6:
        raise ValueError("Expected exactly 6 sense buckets (20 lines each).")
    specs = [(sense, 20, tmpls) for sense, tmpls in sense_templates.items()]
    return build_multisense_from_specs(specs, lesson_every=4)


def build_pasar_bank() -> list[dict]:
    return _bank(
        {
            "happen": (
                "Something unexpected happened on day {i} of the trip.",
                "What happened after we closed the door?",
                "I still do not know what happened behind the curtain.",
                "Nothing happened that could change the outcome.",
            ),
            "spend_time": (
                "We passed two hours in line before the doors opened.",
                "She passed the afternoon reading on the terrace.",
                "They passed the whole weekend without answering email.",
                "I passed twenty minutes looking for parking.",
            ),
            "pass_object": (
                "Please pass the salt when you can.",
                "He passed me the folder under the table.",
                "Could you pass that wrench?",
                "She passed the baby to her partner carefully.",
            ),
            "pass_exam": (
                "I hope I pass the written exam on the first try.",
                "She passed the driving test after three attempts.",
                "They passed the screening and moved to the interview.",
                "He barely passed the course with a seventy.",
            ),
            "come_by_drop": (
                "I'll pass by your office after lunch.",
                "We passed by the bakery but it was closed.",
                "She passes by this park every morning.",
                "They passed by the station without stopping.",
            ),
            "what_about": (
                "So what happens next? — What about passing the memo?",
                "Passing the buck is not an option here.",
                "The rumor passed through the office in an hour.",
                "Let me know what passes for acceptable here.",
            ),
        }
    )


def build_dejar_bank() -> list[dict]:
    return _bank(
        {
            "leave_place": (
                "I left my keys on the counter again.",
                "We left the party before midnight.",
                "She left the room without a word.",
                "They left the country for good.",
            ),
            "let_allow": (
                "My parents let me stay out until ten.",
                "The rules do not let us park here overnight.",
                "She let him explain before interrupting.",
                "We let the dough rise for an hour.",
            ),
            "stop_quit": (
                "He left smoking years ago.",
                "I need to leave worrying about things I cannot control.",
                "They left arguing and shook hands.",
                "She will not leave trying until it works.",
            ),
            "drop_off": (
                "I will drop you off at the corner.",
                "Can you drop this package at the post office?",
                "We dropped the kids off at camp.",
                "She dropped me off near the bridge.",
            ),
            "leave_behind": (
                "Do not leave your passport in the hotel safe.",
                "The flood left mud everywhere.",
                "The scandal left a stain on his reputation.",
                "Winter left the fields bare.",
            ),
            "abandon": (
                "He left the project halfway through.",
                "They left the idea for a better offer.",
                "She left her job to study full time.",
                "We left tradition aside for one night.",
            ),
        }
    )


def build_salir_bank() -> list[dict]:
    return _bank(
        {
            "go_out": (
                "We go out dancing every Friday.",
                "She went out with friends after work.",
                "Do you want to go out tonight?",
                "He rarely goes out in winter.",
            ),
            "leave_exit": (
                "I left the building through the side door.",
                "They left the meeting early.",
                "We need to leave before traffic peaks.",
                "She left the house at dawn.",
            ),
            "turn_out_result": (
                "It turned out cheaper than we thought.",
                "The cake turned out dry.",
                "How did the interview turn out?",
                "Everything turned out fine in the end.",
            ),
            "cost_sale": (
                "The shirt was on sale for fifteen euros.",
                "This repair will cost more than the car is worth.",
                "The tickets came out expensive at the door.",
                "How much did the meal come out to?",
            ),
            "appear_publish": (
                "Her article came out in the Sunday paper.",
                "The new model comes out next month.",
                "Photos came out blurry in the dark.",
                "The truth came out during the trial.",
            ),
            "stand_out": (
                "He stands out in a crowd because of his height.",
                "That detail stands out in the report.",
                "She always wanted to stand out academically.",
                "The red door stands out against the gray wall.",
            ),
        }
    )


def build_poner_bank() -> list[dict]:
    return _bank(
        {
            "put_place": (
                "Put your bag on the hook.",
                "She put the documents in the drawer.",
                "We put the chairs in a circle.",
                "He put his phone face down on the table.",
            ),
            "turn_on": (
                "Please put the kettle on.",
                "She put the radio on low.",
                "They put the heat on because the baby was cold.",
                "I put the lights on at dusk.",
            ),
            "put_on_clothes": (
                "Put on a jacket; it is windy.",
                "She put on her glasses to read.",
                "He put on an old coat to walk the dog.",
                "We put on boots before the hike.",
            ),
            "set_assign": (
                "They put him in charge of logistics.",
                "The judge put a deadline on the filing.",
                "She put herself forward for the role.",
                "We put the meeting on Thursday.",
            ),
            "express_attitude": (
                "He put it bluntly: we are out of time.",
                "She put it nicely, but we understood.",
                "They put pressure on us to decide.",
                "I will put my cards on the table.",
            ),
            "suppose_assume": (
                "I put his age at around forty.",
                "She put two and two together quickly.",
                "They put the blame on the supplier.",
                "We put faith in the process.",
            ),
        }
    )


def build_dar_bank() -> list[dict]:
    return _bank(
        {
            "give_transfer": (
                "Give me your hand; the step is slippery.",
                "She gave him a book for his birthday.",
                "We gave them shelter for the night.",
                "He gave the waiter a generous tip.",
            ),
            "give_abstract": (
                "That noise gives me a headache.",
                "The view gives me peace.",
                "Her smile gave us courage.",
                "The news gave everyone pause.",
            ),
            "hit_strike": (
                "The storm gave the coast a direct hit.",
                "The boxer gave him a jab to the ribs.",
                "The car gave a lurch and stopped.",
                "Reality gave him a hard knock.",
            ),
            "hold_event": (
                "They are giving a concert next week.",
                "The club gives classes on Saturdays.",
                "We give a party when the lease ends.",
                "The museum gives tours in English.",
            ),
            "express_opinion": (
                "I give you my word.",
                "The critics gave the film mixed reviews.",
                "She gave her opinion without sugarcoating.",
                "He gave thanks before the meal.",
            ),
            "fit_turn": (
                "The key gives in the lock now.",
                "The screw gives when you turn it.",
                "The door gives a little when you push.",
                "The fabric gives after a few washes.",
            ),
        }
    )


def build_tener_bank() -> list[dict]:
    return _bank(
        {
            "possess": (
                "I have two brothers in Madrid.",
                "She has a small dog and a large cat.",
                "We have enough chairs for everyone.",
                "They have a cabin by the lake.",
            ),
            "tener_que": (
                "I have to finish this tonight.",
                "She has to see a doctor this week.",
                "We have to decide before Friday.",
                "They have to replace the roof soon.",
            ),
            "age_height": (
                "I am twenty-nine years old.",
                "The tree must be a hundred years old.",
                "She has the patience of a saint.",
                "He has broad shoulders from rowing.",
            ),
            "feel_physical": (
                "I have a fever and chills.",
                "She has a pain in her lower back.",
                "We have hunger after the hike.",
                "He has cold hands.",
            ),
            "relationship_event": (
                "We have a meeting at three.",
                "She has a dentist appointment tomorrow.",
                "They have plans for the holiday.",
                "I have doubts about the proposal.",
            ),
            "hold_opinion": (
                "I have the impression he is lying.",
                "She has no idea how hard this is.",
                "We have reason to be cautious.",
                "He has faith in the team.",
            ),
        }
    )


def build_sacar_bank() -> list[dict]:
    return _bank(
        {
            "take_out": (
                "Take your shoes off before entering.",
                "She took the cake out of the oven.",
                "We took the trash out after dinner.",
                "He took a pen out of his pocket.",
            ),
            "get_obtain": (
                "I got a good grade on the quiz.",
                "She got her license last spring.",
                "They got tickets online.",
                "We got a table by the window.",
            ),
            "photo": (
                "I took a photo of the sunset.",
                "She took several shots of the bird.",
                "We took pictures for the brochure.",
                "He took a selfie in front of the statue.",
            ),
            "derive_conclude": (
                "What conclusion do you draw from the data?",
                "She drew strength from her friends.",
                "We can draw a line under that chapter.",
                "He drew the wrong lesson from the episode.",
            ),
            "stick_out": (
                "His ears stick out a little.",
                "The nail sticks out from the board.",
                "She sticks out in that yellow coat.",
                "The branch sticks out over the path.",
            ),
            "subtract": (
                "If you take three from ten you get seven.",
                "Take the discount off the total.",
                "We took costs out of the estimate.",
                "She took a day off work.",
            ),
        }
    )


def build_seguir_bank() -> list[dict]:
    return _bank(
        {
            "follow": (
                "Follow the signs to the exit.",
                "She follows the news every morning.",
                "We follow the recipe exactly.",
                "They follow him on social media.",
            ),
            "keep_doing": (
                "I keep trying even when it is hard.",
                "She keeps working while the baby sleeps.",
                "We keep hoping for good news.",
                "He keeps asking the same question.",
            ),
            "come_next": (
                "What follows from that premise?",
                "Chapter three follows the introduction.",
                "The sequel follows the hero abroad.",
                "Silence followed his remark.",
            ),
            "obey": (
                "Soldiers follow orders.",
                "The dog follows commands well.",
                "We follow the safety protocol.",
                "She follows her instincts.",
            ),
            "pursue": (
                "The police followed the suspect for blocks.",
                "Dreams followed him all his life.",
                "Success followed years of practice.",
                "Thunder followed the lightning.",
            ),
            "continue": (
                "The road follows the river.",
                "Tradition follows the old ways.",
                "Winter follows autumn every year.",
                "The story follows two families.",
            ),
        }
    )


def build_volver_bank() -> list[dict]:
    return _bank(
        {
            "return_place": (
                "I returned home after midnight.",
                "She came back to the office on Monday.",
                "We returned to the same beach every summer.",
                "They came back empty-handed.",
            ),
            "return_object": (
                "Please return the book by Friday.",
                "She returned the defective lamp.",
                "We returned fire only in self-defense.",
                "He returned the serve with force.",
            ),
            "again": (
                "I read the letter again.",
                "She called again the next day.",
                "We tried again with a new approach.",
                "They met again after twenty years.",
            ),
            "turn_become": (
                "The milk turned sour overnight.",
                "He turned pale when he heard the news.",
                "The discussion turned ugly fast.",
                "Her face turned red.",
            ),
            "do_again": (
                "I will do the calculation again.",
                "She sang the verse again.",
                "We watched the scene again in slow motion.",
                "He asked again more politely.",
            ),
            "revert": (
                "Things returned to normal after the storm.",
                "The city returned to calm.",
                "He returned to his old habits.",
                "Power returned after six hours.",
            ),
        }
    )


def build_andar_bank() -> list[dict]:
    return _bank(
        {
            "walk": (
                "We walked through the old quarter.",
                "She walks to work when it is nice out.",
                "They walked the dog before breakfast.",
                "I walked aimlessly for an hour.",
            ),
            "rumor_go": (
                "Word goes that they will merge.",
                "The story goes that the house is haunted.",
                "How goes the project?",
                "Rumor has it he resigned.",
            ),
            "be_about_state": (
                "He is always about complaining.",
                "She goes around worried about money.",
                "Things are bad all around lately.",
                "I have been about fixing the roof for months.",
            ),
            "function_run": (
                "How is the engine running?",
                "The old truck still runs fine.",
                "The watch runs slow.",
                "The software runs on any machine.",
            ),
            "wander": (
                "His mind wanders during long meetings.",
                "We wandered the market for hours.",
                "Thoughts wandered to childhood.",
                "The conversation wandered off topic.",
            ),
            "get_along": (
                "How are you getting along with your roommate?",
                "They do not get along with the neighbors.",
                "She gets along fine without help.",
                "We get along as colleagues, not friends.",
            ),
        }
    )


def build_ir_bank() -> list[dict]:
    return _bank(
        {
            "go_move": (
                "I go to the gym twice a week.",
                "She goes to Barcelona for work.",
                "We are going to the coast this weekend.",
                "They went home early.",
            ),
            "future_plan": (
                "I am going to call you tomorrow.",
                "She is going to study medicine.",
                "We are going to need more chairs.",
                "It is going to rain later.",
            ),
            "suit_match": (
                "That color goes well with your eyes.",
                "The sauce goes with fish.",
                "This tie goes with the suit.",
                "Red does not go with that pattern.",
            ),
            "road_lead": (
                "Where does this road go?",
                "The path goes through the forest.",
                "The story goes to a dark place.",
                "Time goes fast when you are busy.",
            ),
            "extend_work": (
                "This battery goes for twelve hours.",
                "The money goes to charity.",
                "The lease goes until June.",
                "The rule goes for everyone.",
            ),
            "leave_depart": (
                "The train goes at six sharp.",
                "We must go before it closes.",
                "Time to go; I have another meeting.",
                "He went without saying goodbye.",
            ),
        }
    )


def build_venir_bank() -> list[dict]:
    return _bank(
        {
            "come_arrive": (
                "Come here for a second.",
                "She comes to visit every spring.",
                "We came as soon as we heard.",
                "They are coming by train.",
            ),
            "come_from_origin": (
                "I come from a small town.",
                "This wine comes from Rioja.",
                "The tradition comes from his grandparents.",
                "The problem comes from poor planning.",
            ),
            "just_recently": (
                "I just finished the report.",
                "She had only just arrived when it started.",
                "We had just sat down when the phone rang.",
                "They had just left when you called.",
            ),
            "suit_fit": (
                "That jacket comes tight on you.",
                "The role comes natural to her.",
                "The name comes easy to pronounce.",
                "The work comes hard after illness.",
            ),
            "occur": (
                "Ideas come when you least expect them.",
                "Sleep comes slowly after coffee.",
                "Doubts came later that night.",
                "The answer came in a dream.",
            ),
            "amount_to": (
                "The bill comes to ninety euros.",
                "The total comes to more than we budgeted.",
                "What does that come to with tax?",
                "The repair comes to half the car's value.",
            ),
        }
    )


def build_tomar_bank() -> list[dict]:
    return _bank(
        {
            "take_grasp": (
                "Take my hand crossing the stream.",
                "She took the last cookie.",
                "We took the early flight.",
                "He took responsibility for the error.",
            ),
            "drink": (
                "I take coffee without sugar.",
                "She took a sip and winced.",
                "We took wine with dinner.",
                "They took shots at the party.",
            ),
            "take_transport": (
                "We took the bus downtown.",
                "I took a taxi because it was late.",
                "She took the stairs to the fifth floor.",
                "They took the coastal route.",
            ),
            "take_time": (
                "It took an hour to clear security.",
                "The repair took three days.",
                "The decision took courage.",
                "Recovery took longer than expected.",
            ),
            "assume_view": (
                "I take your point about the budget.",
                "She took him for a tourist.",
                "We take it that you agree.",
                "They took the news calmly.",
            ),
            "capture": (
                "The photo took the whole landscape.",
                "The headline took everyone by surprise.",
                "Winter took the last leaves.",
                "The storm took the roof off.",
            ),
        }
    )


def build_decir_bank() -> list[dict]:
    return _bank(
        {
            "say_words": (
                "What did she say exactly?",
                "Say that again more slowly.",
                "I said nothing during the argument.",
                "He said yes before thinking.",
            ),
            "tell_person": (
                "Tell me the truth.",
                "She told him the whole story.",
                "We told them to wait outside.",
                "They told us the news yesterday.",
            ),
            "rumor_report": (
                "People say the factory will close.",
                "The paper says rain tomorrow.",
                "Legend says treasure lies here.",
                "Critics say the play is bold.",
            ),
            "call_name": (
                "They call him Shorty behind his back.",
                "What do you call this dish?",
                "She calls herself a realist.",
                "We call that progress.",
            ),
            "mean_intend": (
                "I meant no offense.",
                "What do you mean by that?",
                "She means to finish tonight.",
                "This means a lot to us.",
            ),
            "suppose": (
                "I would say he is about fifty.",
                "Let us say we agree for now.",
                "You could say we were lucky.",
                "That is to say, we are out of options.",
            ),
        }
    )


def build_encontrar_bank() -> list[dict]:
    return _bank(
        {
            "find_locate": (
                "I found my keys under the couch.",
                "She found a mistake on page three.",
                "We found shelter in a barn.",
                "They found oil on the property.",
            ),
            "meet_encounter": (
                "I met her at a conference.",
                "We met by chance at the airport.",
                "She met opposition from the board.",
                "He met his match in the final round.",
            ),
            "feel_experience": (
                "I find the heat unbearable here.",
                "She finds joy in small things.",
                "We find it hard to refuse.",
                "They found the climb exhausting.",
            ),
            "consider_judge": (
                "I find the argument weak.",
                "The jury found him guilty.",
                "She found the evidence convincing.",
                "We find your proposal acceptable.",
            ),
            "be_located": (
                "The shop is found on the main square.",
                "Rare species are found only here.",
                "The fault is found along this seam.",
                "Courage is found in unexpected places.",
            ),
            "meet_run_into": (
                "I ran into my cousin at the hardware store.",
                "We ran into red tape at city hall.",
                "She ran into an old teacher on the hiking trail.",
                "They ran into unexpected costs on the project.",
            ),
        }
    )


def build_estar_bank() -> list[dict]:
    return _bank(
        {
            "location": (
                "I am at the library until six.",
                "The keys are on the counter.",
                "We were in Madrid last week.",
                "She is upstairs on the phone.",
            ),
            "temporary_state": (
                "I am tired after the flight.",
                "She is nervous about the interview.",
                "We are ready to leave.",
                "They were sick all winter.",
            ),
            "estar_por": (
                "I am about to send the email.",
                "She is about to graduate.",
                "We were about to give up.",
                "The show is about to start.",
            ),
            "estar_para": (
                "The soup is for lunch tomorrow.",
                "This tool is for cutting metal.",
                "I am not one for small talk.",
                "The room is for guests only.",
            ),
            "progressive": (
                "I am studying for the exam.",
                "She was working when I called.",
                "We are fixing the leak today.",
                "They were talking for hours.",
            ),
            "result_condition": (
                "The soup is cold now.",
                "The door is open.",
                "The paint is wet.",
                "The store is closed on Sundays.",
            ),
        }
    )


def build_ser_bank() -> list[dict]:
    return _bank(
        {
            "identity_profession": (
                "She is a doctor.",
                "I am from Canada originally.",
                "We are students at the university.",
                "He was a soldier before the injury.",
            ),
            "essential_quality": (
                "The problem is simple on paper.",
                "That is true in theory.",
                "Iron is hard; butter is soft.",
                "The idea is brilliant.",
            ),
            "time_date": (
                "It is three o'clock.",
                "Today is Tuesday.",
                "It was midnight when we arrived.",
                "The meeting is next Friday.",
            ),
            "passive_ser": (
                "The bridge was built in 1920.",
                "The letter was written by hand.",
                "Mistakes were made on both sides.",
                "The law was passed last year.",
            ),
            "impersonal_estructura": (
                "It is important to listen.",
                "It is necessary to register first.",
                "It was impossible to see in the fog.",
                "It is better to wait.",
            ),
            "possession_belong": (
                "This land is mine.",
                "The fault is yours alone.",
                "The choice is hers to make.",
                "The honor is all theirs.",
            ),
        }
    )


POLYSEMOUS_BUILDERS_EXT: dict[str, Callable[[], list[dict]]] = {
    "pasar": build_pasar_bank,
    "dejar": build_dejar_bank,
    "salir": build_salir_bank,
    "poner": build_poner_bank,
    "dar": build_dar_bank,
    "tener": build_tener_bank,
    "sacar": build_sacar_bank,
    "seguir": build_seguir_bank,
    "volver": build_volver_bank,
    "andar": build_andar_bank,
    "ir": build_ir_bank,
    "venir": build_venir_bank,
    "tomar": build_tomar_bank,
    "decir": build_decir_bank,
    "encontrar": build_encontrar_bank,
    "estar": build_estar_bank,
    "ser": build_ser_bank,
}
