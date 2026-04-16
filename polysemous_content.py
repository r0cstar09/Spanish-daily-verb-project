"""
Curated English prompts for Spanish verbs whose gloss does not map to one English verb.

Each item is (english_prompt, sense_tag). Tags are short labels for the email and for review.
Used by scripts/build_sentence_banks.py instead of generic {base} templates.
"""

from __future__ import annotations

from polysemous_banks_extended import POLYSEMOUS_BUILDERS_EXT
from polysemous_helpers import add_lessons_every, bank_from_rows


def build_quedar_bank() -> list[dict]:
    """Spanish quedar: stay, be left, agree, meet, fit, result/location — English cues vary."""
    rows: list[tuple[str, str]] = []

    # stay / remain (often quedarse)
    stay = [
        ("I stayed home last night while everyone else went to the concert.", "stay"),
        ("She stayed behind after class to ask the professor a question.", "stay"),
        ("We stayed at a small hotel near the train station.", "stay"),
        ("He decided to stay in instead of going out in the rain.", "stay"),
        ("They stayed up late finishing the presentation.", "stay"),
        ("I stayed quiet during the argument because I did not know the facts.", "stay"),
        ("She stayed in bed all morning with a fever.", "stay"),
        ("We stayed friends even after we stopped working together.", "stay"),
        ("He stayed at the office until the backup finished.", "stay"),
        ("I stayed on the line for twenty minutes before anyone answered.", "stay"),
        ("She stayed near the exit in case we had to leave quickly.", "stay"),
        ("We stayed together through several difficult moves.", "stay"),
        ("He stayed under the umbrella while I ran to the car.", "stay"),
        ("I stayed awake reading until two in the morning.", "stay"),
        ("They stayed loyal to the team despite the losses.", "stay"),
        ("She stayed calm when the alarm went off.", "stay"),
        ("We stayed in touch by video call every Sunday.", "stay"),
        ("He stayed put until the police arrived.", "stay"),
        ("I stayed out of the discussion because it was not my decision.", "stay"),
        ("They stayed overnight at my parents' house.", "stay"),
    ]
    rows.extend(stay)

    # quantity left / remaining
    leftover = [
        ("There's only one slice of cake left.", "leftover"),
        ("We have three chairs left to assemble.", "leftover"),
        ("How much time do we have left before the store closes?", "leftover"),
        ("There's no milk left in the fridge.", "leftover"),
        ("She counted how many vacation days she had left.", "leftover"),
        ("There's plenty of pasta left if you want seconds.", "leftover"),
        ("Not much daylight was left when we reached the trailhead.", "leftover"),
        ("We sold every copy except two that were left on the shelf.", "leftover"),
        ("There's nothing left to say after that apology.", "leftover"),
        ("I have one question left before we wrap up.", "leftover"),
        ("There's half a tank of gas left.", "leftover"),
        ("They divided what was left among the volunteers.", "leftover"),
        ("There's room left in the suitcase for a jacket.", "leftover"),
        ("We ate what was left of the bread for breakfast.", "leftover"),
        ("There's a little paint left in the can.", "leftover"),
        ("She spent what was left of her savings on the repair.", "leftover"),
        ("There's one ticket left for the matinee.", "leftover"),
        ("I used what was left of my patience on that phone call.", "leftover"),
        ("There's still some battery left on the phone.", "leftover"),
        ("They donated what was left after covering the costs.", "leftover"),
    ]
    rows.extend(leftover)

    # agree (quedar en)
    agree = [
        ("We agreed to meet at the library entrance at noon.", "agree"),
        ("They agreed not to discuss salary during the interview.", "agree"),
        ("I agreed to call as soon as I landed.", "agree"),
        ("We agreed on a price after a short negotiation.", "agree"),
        ("She agreed to send the files before Friday.", "agree"),
        ("They agreed to split the bill evenly.", "agree"),
        ("We agreed that he would drive the first leg.", "agree"),
        ("I agreed to take the early shift next week.", "agree"),
        ("They agreed to postpone the vote until Monday.", "agree"),
        ("We agreed on a color for the living room walls.", "agree"),
        ("She agreed to keep the news private for now.", "agree"),
        ("They agreed to review the contract with a lawyer.", "agree"),
        ("We agreed to rotate who hosts the meeting.", "agree"),
        ("I agreed to lend my tools if they returned them clean.", "agree"),
        ("They agreed to extend the deadline by two days.", "agree"),
        ("We agreed not to bring up politics at dinner.", "agree"),
        ("She agreed to translate the summary for free.", "agree"),
        ("They agreed to meet halfway between the two cities.", "agree"),
        ("We agreed on a signal if something went wrong.", "agree"),
        ("I agreed to wait until she had talked to her boss.", "agree"),
    ]
    rows.extend(agree)

    # meet someone (quedar con)
    meet = [
        ("I'm meeting my dentist at three tomorrow.", "meet"),
        ("She had to reschedule the time we had planned to meet.", "meet"),
        ("We are meeting them at the airport arrivals gate.", "meet"),
        ("I forgot I was meeting someone for coffee.", "meet"),
        ("He's meeting a client downtown after lunch.", "meet"),
        ("Are you meeting your brother this weekend?", "meet"),
        ("We were supposed to meet at six, but the train was late.", "meet"),
        ("I'm meeting her halfway between our two apartments.", "meet"),
        ("They met every Tuesday to practice conversation.", "meet"),
        ("I can't meet earlier; I have another appointment.", "meet"),
        ("She suggested meeting online instead of in person.", "meet"),
        ("We're meeting the contractor at the house at nine.", "meet"),
        ("He never showed up to meet me at the agreed corner.", "meet"),
        ("I'm meeting old classmates at the reunion.", "meet"),
        ("We could meet for ten minutes between your meetings.", "meet"),
        ("I'll meet you outside the museum ticket desk.", "meet"),
        ("They decided to meet on neutral ground.", "meet"),
        ("I'm meeting someone who might buy the bike.", "meet"),
        ("We should meet before you sign anything.", "meet"),
        ("She's meeting the landlord to hand over the keys.", "meet"),
    ]
    rows.extend(meet)

    # fit / suit (clothing, appearance)
    fit = [
        ("The jacket fits me well across the shoulders.", "fit"),
        ("Those pants don't fit anymore after the holidays.", "fit"),
        ("The dress fits perfectly without alterations.", "fit"),
        ("This color fits your complexion better than the last one.", "fit"),
        ("The boots fit tightly until I broke them in.", "fit"),
        ("The ring fits only on my middle finger.", "fit"),
        ("The hat fits loosely, so it might fly off in the wind.", "fit"),
        ("The shirt fits like it was made for you.", "fit"),
        ("Those gloves don't fit; try the next size.", "fit"),
        ("The costume fit awkwardly because we rushed the measurements.", "fit"),
        ("The new sofa fits the room better than the old one.", "fit"),
        ("The frame fits the painting exactly.", "fit"),
        ("The lid fits snugly on the container.", "fit"),
        ("The strap fits comfortably around my wrist.", "fit"),
        ("The child has grown; the coat no longer fits.", "fit"),
        ("The shelves fit flush against the wall.", "fit"),
        ("The key fits, but the lock still sticks.", "fit"),
        ("The cover fits the phone model listed on the box.", "fit"),
        ("The wig fits so well I barely recognize you.", "fit"),
        ("The spare tire fits in the trunk under the mat.", "fit"),
    ]
    rows.extend(fit)

    # result, placement, figurative (quedar bien/mal, quedar en ridículo, ranking)
    result = [
        ("The hotel turned out to be right on the waterfront.", "result"),
        ("I ended up looking foolish when I defended the wrong number.", "result"),
        ("The interview left a better impression than I expected.", "result"),
        ("We came in third place in the regional finals.", "result"),
        ("The joke landed badly in that crowd.", "result"),
        ("The explanation left everyone confused.", "result"),
        ("The photos came out blurry because of the low light.", "result"),
        ("The negotiation left both sides unhappy.", "result"),
        ("The city ended up being smaller than it looked on the map.", "result"),
        ("His comment left her speechless.", "result"),
        ("The project left us with more debt than profit.", "result"),
        ("The trip left me exhausted for two days.", "result"),
        ("The movie left a strong impression on the jury.", "result"),
        ("The scandal left the company in a weak position.", "result"),
        ("The hike left us sore but glad we went.", "result"),
        ("The decision left no room for appeal.", "result"),
        ("The gift left her wondering how much we had spent.", "result"),
        ("The answer left several questions unanswered.", "result"),
        ("The evening left us with good memories despite the rain.", "result"),
        ("The error left the totals off by a few hundred dollars.", "result"),
    ]
    rows.extend(result)

    assert len(rows) == 120, len(rows)
    return bank_from_rows(add_lessons_every(rows, every=4))


def build_hacer_bank() -> list[dict]:
    """Spanish hacer: do, make, weather (hace), time (hace), collocations, figurative."""
    rows: list[tuple[str, str]] = []

    do_act = [
        ("I did the dishes while you put the kids to bed.", "do"),
        ("She does yoga three mornings a week.", "do"),
        ("We need to do the paperwork before the deadline.", "do"),
        ("He did his best under difficult conditions.", "do"),
        ("What are you doing this weekend?", "do"),
        ("They did a thorough inspection of the brakes.", "do"),
        ("I have done that route so many times I could drive it blind.", "do"),
        ("She does volunteer work at the shelter.", "do"),
        ("We did what we could with the budget we had.", "do"),
        ("He refuses to do overtime unless they pay for it.", "do"),
        ("I did not do anything wrong.", "do"),
        ("They are doing research on coastal erosion.", "do"),
        ("She did me a huge favor by covering my shift.", "do"),
        ("We should do a trial run before the real event.", "do"),
        ("He does not do well on little sleep.", "do"),
        ("I did the calculations twice to be sure.", "do"),
        ("They do not do refunds without a receipt.", "do"),
        ("She did an internship at the embassy.", "do"),
        ("We will do another pass over the report tonight.", "do"),
        ("He did exactly what the manual said.", "do"),
    ]
    rows.extend(do_act)

    make_create = [
        ("She made soup from whatever was in the fridge.", "make"),
        ("They made a documentary about small-town musicians.", "make"),
        ("We made a list of everything we still need.", "make"),
        ("He made a mistake on the first page of the form.", "make"),
        ("I made a promise I intend to keep.", "make"),
        ("The company made a profit for the first time in years.", "make"),
        ("She made room on the shelf for the new books.", "make"),
        ("We made eye contact across the crowded room.", "make"),
        ("He made an effort to arrive on time.", "make"),
        ("They made changes to the design after the test.", "make"),
        ("I made friends with my neighbors quickly.", "make"),
        ("She made a scene when they lost her reservation.", "make"),
        ("We made progress even though it felt slow.", "make"),
        ("He made a habit of walking before breakfast.", "make"),
        ("They made sure the door was locked.", "make"),
        ("I made copies for everyone in the meeting.", "make"),
        ("She made art from recycled metal.", "make"),
        ("We made a pact not to tell anyone yet.", "make"),
        ("He made breakfast while I packed the car.", "make"),
        ("They made history with that comeback.", "make"),
    ]
    rows.extend(make_create)

    # Weather — English "It's hot/cold" → Spanish hace calor/frío
    weather = [
        ("It's freezing outside; wear a scarf.", "weather"),
        ("It's scorching today; the pavement shimmers.", "weather"),
        ("How cold it was on the mountain pass!", "weather"),
        ("It's muggy and hard to breathe after the storm.", "weather"),
        ("It's pleasant in the shade but brutal in the sun.", "weather"),
        ("It's windy enough to cancel the boat trip.", "weather"),
        ("It's damp this morning; the laundry will not dry.", "weather"),
        ("It's unusually warm for February.", "weather"),
        ("It's dark and stormy; stay off the ridge.", "weather"),
        ("It's bright and clear — perfect for photos.", "weather"),
        ("It's chilly in the hall; bring a sweater.", "weather"),
        ("It's oppressive before the thunderstorm breaks.", "weather"),
        ("It's cool at night even when the days are hot.", "weather"),
        ("It's foggy near the river at dawn.", "weather"),
        ("It's harsh sunlight; wear sunscreen.", "weather"),
        ("It's mild today compared with yesterday.", "weather"),
        ("It's rainy season; expect mud on the trail.", "weather"),
        ("It's blistering in the plaza at noon.", "weather"),
        ("It's raw and gray along the coast.", "weather"),
        ("It's stifling inside with the windows closed.", "weather"),
    ]
    rows.extend(weather)

    # Time / duration — English "It's been X since" → hace...
    time_span = [
        ("It's been two years since I visited that city.", "time"),
        ("It's been a while since we last spoke.", "time"),
        ("It's been months since they fixed the elevator.", "time"),
        ("It's been only a week, but it feels longer.", "time"),
        ("It's been ages since I rode a bike.", "time"),
        ("It's been a long morning already.", "time"),
        ("It's been twenty minutes; should we call again?", "time"),
        ("It's been three days since the package shipped.", "time"),
        ("It's been forever since we had a vacation.", "time"),
        ("It's been short notice, but can you come?", "time"),
        ("It's been over an hour in this queue.", "time"),
        ("It's been years since the bridge was painted.", "time"),
        ("It's been a tough quarter for sales.", "time"),
        ("It's been quiet since the neighbors moved out.", "time"),
        ("It's been half a day and still no reply.", "time"),
        ("It's been since Tuesday that I slept well.", "time"),
        ("It's been a minute since I checked the oven.", "time"),
        ("It's been rough since the schedule changed.", "time"),
        ("It's been clear since yesterday that we need help.", "time"),
        ("It's been a decade since the last renovation.", "time"),
    ]
    rows.extend(time_span)

    # Collocations / periphrasis (hacer caso, hacer falta, hacer daño cues)
    colloc = [
        ("You should pay attention to what the doctor tells you.", "colloc"),
        ("We really need an extra pair of hands this afternoon.", "colloc"),
        ("That fall might hurt more tomorrow than today.", "colloc"),
        ("Children need structure, not just freedom.", "colloc"),
        ("Ignoring safety rules can get someone hurt.", "colloc"),
        ("We lack the tools to finish the repair today.", "colloc"),
        ("She needs space to think without interruptions.", "colloc"),
        ("The remark stung more than he admitted.", "colloc"),
        ("They need proof before they can act.", "colloc"),
        ("Cold air can harm sensitive plants.", "colloc"),
        ("We need patience with a new team.", "colloc"),
        ("Loud music late at night bothers the neighbors.", "colloc"),
        ("He needs practice, not criticism.", "colloc"),
        ("Sunburn can harm your skin over the years.", "colloc"),
        ("We need a plan B before we announce anything.", "colloc"),
        ("Sharp tools can hurt if you are careless.", "colloc"),
        ("They need time to process the news.", "colloc"),
        ("Envy can poison a friendship.", "colloc"),
        ("We need one more signature on the form.", "colloc"),
        ("Neglect can damage an engine over time.", "colloc"),
    ]
    rows.extend(colloc)

    # Pretend, role, noise (hacerse, hacer de, hacer ruido)
    misc = [
        ("He pretends not to hear when the topic is money.", "misc"),
        ("She plays the villain in the school play.", "misc"),
        ("They made a lot of noise moving the piano.", "misc"),
        ("Stop fooling yourself about how much time you have.", "misc"),
        ("He acted as interpreter during the visit.", "misc"),
        ("The kids made a racket in the hallway.", "misc"),
        ("She turned into a confident speaker over the year.", "misc"),
        ("They staged a protest outside city hall.", "misc"),
        ("He made fun of my accent, then apologized.", "misc"),
        ("We made a campfire by the lake.", "misc"),
        ("She made herself comfortable on the couch.", "misc"),
        ("They made a circle to discuss the issue.", "misc"),
        ("He made a face when he tasted the medicine.", "misc"),
        ("We made small talk until the host arrived.", "misc"),
        ("She made a gesture inviting him to sit.", "misc"),
        ("They made waves in the industry with that product.", "misc"),
        ("He made believe he was asleep.", "misc"),
        ("We made a bet on the outcome of the match.", "misc"),
        ("She made a point of thanking everyone.", "misc"),
        ("They made trouble for the new manager at first.", "misc"),
    ]
    rows.extend(misc)

    assert len(rows) == 120, len(rows)
    return bank_from_rows(add_lessons_every(rows, every=4))


POLYSEMOUS_BUILDERS = {
    "quedar": build_quedar_bank,
    "hacer": build_hacer_bank,
    **POLYSEMOUS_BUILDERS_EXT,
}


def build_polysemous_bank(verb: str) -> list[dict] | None:
    fn = POLYSEMOUS_BUILDERS.get(verb.strip().lower())
    if fn is None:
        return None
    return fn()
