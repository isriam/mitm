#!/usr/bin/env python3
from __future__ import annotations
from pydantic import BaseModel, Field, root_validator, ValidationError
from typing import Optional
import csv


class RuneAbility(BaseModel):
    identifier: str
    ability: str
    abilityOperator: str
    abilityText: str
    abilityUnit: str
    enhanceValues: str

    def __repr__(self):
        return f"{self.abilityText}"

    def getStat(self):
        modifier = 1
        if self.abilityUnit == '%':
            modifier = 100

        vals = [float(x) for x in self.enhanceValues.split("|")]
        base = f"{round(vals[0] * modifier, 1)}{self.abilityUnit}"
        maxed = f"{round(vals[-1] * modifier, 1)}{self.abilityUnit}"
        return f"{self.abilityText} {base}|{maxed}"


class Rune(BaseModel):
    identifier: str
    runeName: str
    abilities: list[RuneAbility]
    runeType: str
    runeSlot: str
    availableTypes: Optional[str]
    availableDragons: str
    rarityIndex: int
    salvageValueId: Optional[str]
    enhanceCosts: Optional[str]
    aura: str
    icon: str

    @root_validator(pre=True)
    def ensureAbilities(cls, values):
        ret = []
        abilities = values.get('abilityIds').split('|')
        for a in abilities:
            for x in rune_abilities:
                if a == x.identifier:
                    ret.append(x)
                    break
            else:
                print(f"Ability not found: {a}")
        values["abilities"] = ret
        return values

    def getStats(self):
        return [a.getStat() for a in self.abilities]

    def __repr__(self):
        return f"{self.runeName} {self.abilities}"


def getRune(rune_id: str) -> Rune:
    for r in runes:
        if rune_id == r.identifier:
            return r

try:
    with open('/mnt/nas/admin/wardragons/wdscripts/RuneAbility.csv', 'r') as f:
        c = csv.DictReader(f, delimiter=",")
        rune_abilities = [RuneAbility(**x)
                          for x in c if x['identifier'] != "String"]
except Exception as e:
    with open('RuneAbility.csv', 'r') as f:
        c = csv.DictReader(f, delimiter=",")
        rune_abilities = [RuneAbility(**x)
                          for x in c if x['identifier'] != "String"]

try:
    with open('Rune.csv', 'r') as f:
        c = csv.DictReader(f, delimiter=",")
        runes = [Rune(**x) for x in c if x['identifier'] != "String"]
except Exception as e:
    with open('/mnt/nas/admin/wardragons/wdscripts/Rune.csv', 'r') as f:
        c = csv.DictReader(f, delimiter=",")
        runes = [Rune(**x) for x in c if x['identifier'] != "String"]

season = "valorcrest"
real_names_dict = {'breedingToken': 'Egg Tokens', 'innerFire01': 'Inner Fire', season + 'Sigil': 'Sigil',
                   'expediteConsumable0': '3 Min Speedup', 'xpMultiplierSpellConsumable01': '+100% XP Boost',
                   'elementalEmber': 'Elemental Ember', 'electrumBar': 'Electrum Bars', 'fireShard': 'Fire Shards',
                   'xpMultiplierSpellConsumable02': '+200% XP Boost', 'iceShard': 'Ice Shards',
                   'expediteConsumable1': '15 Min Speedup', 'expediteConsumable2': '1 Hr Speedup',
                   'expediteConsumable3': '3 Hr Speedup', 'expediteConsumable4': '12 Hr Speedup',
                   'expediteConsumable1a': '30 Min Speedup',
                   'goldPack_500000': '500k gold pack', 'redRiderShard': "Red Rider Shard", 'blueRiderShard': "Blue Rider Shard",
                   'cmCrystalwindGemstone': "Wind Crafting Gemstones", 'cmCrystalfireGemstone': "Fire Crafting Gemstones",
                   'cmCrystalearthGemstone': "Earth Crafting Gemstones", 'cmCrystaldarkGemstone': "Dark Crafting Gemstones",
                   'cmCrystaliceGemstone': "Ice Crafting Gemstones", 'bullhorn': 'Bullhorn', 'missionToken5Star': "5 Star Mission Token",
                   'repairConsumable': 'Defense Hammer', 'blackPearl': 'Black Pearls', 'energyPack': 'Energy Pack',
                   'mysticFragment': 'Mystic Fragments', 'runeDust': 'Rune Dust', 'chisel': 'Chisel',
                   'foodConsumable1': 'Food Pack [Rare]', 'foodConsumable2': 'Food Pack [Epic]',
                   'foodPack_1400000': 'Food Pack [Legendary]', 'foodPack_460000': 'Food Pack [Epic]',
                   'foodPack_22000': 'Food Pack 22k', 'foodPack_90000': 'Food Pack [Rare]', 'fullHeal': 'Healing Potion',
                   'increaseAttack1': '+30% Dragon Atk', 'increaseHP1': '+30% Dragon HP',
                   'increaseBuildingAttack1': '+30% Tower Atk', 'attackConsumable': 'Defense Gunpowder',
                   'increaseBuildingHP1': '+30% Tower HP', 'armorConsumable': 'Defense Armor',
                   'cmCrystaldark': 'Dark Crafting Shards', 'cmCrystalearth': 'Earth Crafting Shards',
                   'cmCrystalwind': 'Wind Crafting Shards', 'cmCrystalfire': 'Fire Crafting Shards',
                   'cmCrystalice': 'Ice Crafting Shards', 'craftingScroll': 'Crafting Scroll',
                   'lumberPack_1400000': 'Lumber Pack [Legendary]', 'lumberConsumable2': 'Lumber Pack [Epic]', 'lumberConsumable1': 'Lumber Pack [Rare]',
                   'E23Q2FestiveHunterDragonEvolutionFragment': 'Vesolance Shard',
                   'E22Q1FestiveWarriorDragonEvolutionFragment': 'Garrvox Shard',
                   'E21Q4FestiveHunterDragonEvolutionFragment': 'Krampi Shard',
                   'E22Q4FestiveHunterDragonEvolutionFragment': 'Re\'gyn Shard',
                   'E23Q1InvokerDragonEvolutionFragment': 'Etzalis Shard',
                   'E22Q2FestiveHunterDragonEvolutionFragment': 'Grumuk Shard',
                   'E22Q3FestiveInvokerDragonEvolutionFragment': 'Pezizo Shard',
                   'E23Q3FestiveSorcererDragonEvolutionFragment': 'Jinhen Shard',
                   'E23Q4FestiveHunterDragonEvolutionFragment': 'Bonewrack',
                   season + 'BronzeRelicKey': 'Bronze Key', season + 'SilverRelicKey': 'Silver Key',
                   season + 'GoldRelicKey': 'Gold Key', season + 'LegacyRelicKey': 'Legacy Key'}


class ChestPredictor(object):
    def __init__(self, params=None, about=None, world_params=None):
        self.about = about
        self.atlas = world_params
        self.params_gacha = params.get("params_and_data").get("gacha")
        # self.params_gacha = params

    class drop(BaseModel):
        drop_type: str
        drop_id: str = Field(alias="id")
        drop_count: int = Field(alias="mu")
        friendly_name: str
        drop_detail: list[str] = []
        credit_drop: bool = Field(default=False)
        seq: int = Field(default=0)

        @root_validator(pre=True)
        def getDropName(cls, values):
            itemid = values.get("id")
            if (r := getRune(itemid)):
                values["friendly_name"] = r.runeName
                values["id"] = r.icon
                values["drop_detail"] = r.getStats()
            else:
                values["friendly_name"] = real_names_dict.get(
                    values.get("id"), "")

            if not values.get("drop_type"):
                values["drop_type"] = ""

            if not values.get("mu") and (c := values.get("count")):
                values["mu"] = c

            return values

        def colored_drop_type(self):
            def prYellow(skk): return "\033[93m {}\033[00m" .format(skk)
            # def prLightPurple(skk): print("\033[94m {}\033[00m" .format(skk))
            def prPurple(skk): return "\033[95m {}\033[00m" .format(skk)
            def prCyan(skk): return "\033[96m {}\033[00m" .format(skk)

            match self.drop_type:
                case "Epic":
                    return prPurple(self.drop_type)
                case "Legendary":
                    return prYellow(self.drop_type)
                case "Mythic":
                    return prCyan(self.drop_type)
                case _:
                    return self.drop_type

        def setCredit(self, credit: bool = False) -> ChestPredictor.drop:
            self.credit_drop = credit
            return self

        def __repr__(self):
            return self.__str__()

        def __str__(self):
            s = f"{self.colored_drop_type():<24s} {('CREDIT' if self.credit_drop else ''):6} {self.drop_count:4} {self.drop_id}"
            if self.credit_drop:
                s += " CREDIT"
            return s

    class deck(BaseModel):
        name: str
        current_idx: int
        sequence: list[int]
        drops: list[ChestPredictor.drop]

        def __init__(self, **kwargs):
            self.update_forward_refs()
            super().__init__(**kwargs)

        def getDrops(self, count: int = 1, st=None):
            my_drops = []
            for i in range(self.current_idx+1, self.current_idx+count+1):
                d = self.drops[self.sequence[i % len(self.sequence)]]
                my_drops.append(
                    d.copy(update={"seq": (i+1) % len(self.sequence)}))
            self.current_idx = self.current_idx+count
            return my_drops

    class spin_type(BaseModel):
        spin_type: int
        spin_type_drop: str
        credit_spin_type: Optional[int]
        credit_spin_type_drop: Optional[str]
        title: str
        # position: int

        # def __repr__(self):
        #     return self.__str__()

        # def __str__(self):
        #     return f"{self.title} (P: {self.position})"

    class event_gacha(BaseModel):
        event: str
        spin_type: ChestPredictor.spin_type
        spin_counts: dict
        deck_indices: dict
        event_decks: list[ChestPredictor.deck]

        def __init__(self, **kwargs):
            self.update_forward_refs()
            super().__init__(**kwargs)

        def getDrops(self, count: int = 1, credit_drop=False) -> list[(ChestPredictor.drop, int)]:
            def resolve_drop(drop):
                if type(drop) != ChestPredictor.drop:
                    return resolve_drop(drop)
                else:
                    return drop

            ret = []
            opened = self.spin_counts[str(self.spin_type.spin_type)]
            while count > 0:
                if opened > 0 and self.spin_type.credit_spin_type and opened % 30 == 0:
                    deck = self.getDeck(self.spin_type.credit_spin_type_drop)
                    opened = 0
                    credit_spin = True
                else:
                    deck = self.getDeck(self.spin_type.spin_type_drop)
                    credit_spin = False
                # print(f"Opened: {opened}, {credit_spin}")

                drop = deck.getDrops(1)[0]
                if dropdeck := self.getDeck(drop.drop_id):
                    x = resolve_drop(dropdeck.getDrops(1)[0])
                    ret.append(
                        x.copy(update={"credit_drop": credit_spin}))
                else:
                    drop = resolve_drop(drop)
                    ret.append(
                        drop.copy(update={"credit_drop": credit_spin}))
                opened += 1
                count -= 1
            return ret

        def getDeck(self, deck_name: str) -> ChestPredictor.deck:
            for d in self.event_decks:
                if d.name == deck_name:
                    return d

    def getEvents(self):
        return [x for x in self.about.keys()]

    def getSpinType(self, event: str, spin_type_title: str):
        for s in self.params_gacha.get(event).get("spin_types"):
            # print(s)
            if spin_type_title == s.get("title"):
                st = s.get("spin_type")
                about_spin_types = self.about.get(event).get(
                    "gacha").get("params").get("spin_types")
                # print(st)
                st_drop = list(about_spin_types[int(st)].get(
                    'drops').get('default').items())[0][0]
                if (c_st := s.get("credit_spin_type")) and c_st >= 0 and len(about_spin_types) >= c_st:
                    c_st_drop = list(about_spin_types[c_st].get(
                        'drops').get('default').items())[0][0]
                else:
                    c_st = None
                    c_st_drop = None
                return ChestPredictor.spin_type(title=spin_type_title, spin_type=s.get("spin_type"), spin_type_drop=st_drop, credit_spin_type=c_st, credit_spin_type_drop=c_st_drop)
        return None

    def getGacha(self, event, spin_type_title):
        if event == "atlas":
            if spin_type_title == "ATLAS CHEST":
                st = ChestPredictor.spin_type(
                    title="ATLAS CHEST", spin_type=1, spin_type_drop="atlas_chest", credit_spin_type=3, credit_spin_type_drop="atlas_chest")
            elif spin_type_title == "ATLAS BADGE CHEST":
                st = ChestPredictor.spin_type(
                    title="ATLAS CHEST", spin_type=2, spin_type_drop="atlasBadge_chest", credit_spin_type=4, credit_spin_type_drop="atlasBadge_chest")
            spin_counts = self.atlas.get("myEventData").get("gacha_total_counts")
            deck_indices = self.atlas.get("params").get("gacha").get("deck_indices")
            event_decks = []
            for d, s in self.atlas.get("params").get("gacha").get("decks").items():
                drops = [ChestPredictor.drop(
                    **x) for x in self.atlas.get("params").get("gacha").get("drops").get(d)]
                current_idx = deck_indices.get(d, 0)
                event_decks.append(ChestPredictor.deck(
                    name=d, sequence=s, drops=drops, current_idx=current_idx))

            return ChestPredictor.event_gacha(event=event, spin_type=st,
                                              spin_counts=spin_counts, event_decks=event_decks, deck_indices=deck_indices)

        elif spin_type_title == "EASTER CHEST":
            st = ChestPredictor.spin_type(
                title="EASTER CHEST", spin_type=31, spin_type_drop="easter_chest", credit_spin_type=32, credit_spin_type_drop="easter_chest")
            spin_counts = self.about.get(event).get("gacha").get("player_data").get("spin_counts")
            deck_indices = self.about.get(event).get("gacha").get("params").get("deck_indices")
            event_decks = []
            for d, s in self.about.get(event).get("gacha").get("params").get("decks").items():
                # print(event, d,s)
                drops = [ChestPredictor.drop(**x) for x in self.params_gacha.get(event).get("drops").get(d)]
                # print(drops)
                current_idx = deck_indices.get(d, 0)
                # print(current_idx)
                event_decks.append(ChestPredictor.deck(name=d, sequence=s, drops=drops, current_idx=current_idx))
                # print(event_decks)

            return ChestPredictor.event_gacha(event=event, spin_type=st,
                                              spin_counts=spin_counts, event_decks=event_decks, deck_indices=deck_indices)

        elif spin_type_title == "FREEDOM CHEST":
            st = ChestPredictor.spin_type(
                title="FREEDOM CHEST", spin_type=33, spin_type_drop="freedom_chest", credit_spin_type=34, credit_spin_type_drop="freedom_chest")
            spin_counts = self.about.get(event).get("gacha").get("player_data").get("spin_counts")
            deck_indices = self.about.get(event).get("gacha").get("params").get("deck_indices")
            event_decks = []
            for d, s in self.about.get(event).get("gacha").get("params").get("decks").items():
                # print(event, d,s)
                drops = [ChestPredictor.drop(**x) for x in self.params_gacha.get(event).get("drops").get(d)]
                # print(drops)
                current_idx = deck_indices.get(d, 0)
                # print(current_idx)
                event_decks.append(ChestPredictor.deck(name=d, sequence=s, drops=drops, current_idx=current_idx))
                # print(event_decks)

            return ChestPredictor.event_gacha(event=event, spin_type=st,
                                              spin_counts=spin_counts, event_decks=event_decks, deck_indices=deck_indices)

        elif spin_type_title == "SPECIAL CHEST":
            st = ChestPredictor.spin_type(
                title="SPECIAL CHEST", spin_type=35, spin_type_drop="frosty_chest", credit_spin_type=36, credit_spin_type_drop="frosty_chest")
            spin_counts = self.about.get(event).get("gacha").get("player_data").get("spin_counts")
            deck_indices = self.about.get(event).get("gacha").get("params").get("deck_indices")
            event_decks = []
            # print('here')
            for d, s in self.about.get(event).get("gacha").get("params").get("decks").items():
                # print(event, d,s)
                drops = [ChestPredictor.drop(**x) for x in self.params_gacha.get(event).get("drops").get(d)]
                # print(drops)
                current_idx = deck_indices.get(d, 0)
                # print(current_idx)
                event_decks.append(ChestPredictor.deck(name=d, sequence=s, drops=drops, current_idx=current_idx))
                # print(event_decks)

            return ChestPredictor.event_gacha(event=event, spin_type=st,
                                              spin_counts=spin_counts, event_decks=event_decks, deck_indices=deck_indices)

        elif st := self.getSpinType(event=event, spin_type_title=spin_type_title):
            spin_counts = self.about.get(event).get("gacha").get("player_data").get("spin_counts")
            deck_indices = self.about.get(event).get("gacha").get("params").get("deck_indices")
            event_decks = []
            for d, s in self.about.get(event).get("gacha").get("params").get("decks").items():
                # print(event, d,s)
                drops = [ChestPredictor.drop(**x) for x in self.params_gacha.get(event).get("drops").get(d)]
                # print(drops)
                current_idx = deck_indices.get(d, 0)
                # print(current_idx)
                event_decks.append(ChestPredictor.deck(name=d, sequence=s, drops=drops, current_idx=current_idx))
                # print(event_decks)

            return ChestPredictor.event_gacha(event=event, spin_type=st,
                                              spin_counts=spin_counts, event_decks=event_decks, deck_indices=deck_indices)

        else:
            print("Spin type not found")

    def getDrops(self, spin_type_title, drop_count=10):
        if "ATLAS" in spin_type_title:
            events = ["atlas"]
        else:
            events = self.getEvents()
        drops = []
        for event in events:
            # print(event)
            event_drops = {"drops": [], "credit_drops": []}
            if (gacha := self.getGacha(event=event, spin_type_title=spin_type_title)):
                print(f"EVENT: {event}")
                print(spin_type_title)
                for i, e in enumerate(gacha.getDrops(drop_count), 1):
                    # print(i)
                    # print(vars(e))
                    # print(f"{i:3}: {str(e):<12s} (SEQ #: {e.seq:3})")
                    event_drops["drops"].append({**e.dict()})
            # print(event)
            drops.append({"event": event, "spin_type": spin_type_title, **event_drops})
            # print(drops)
            # print(20*"-")
        return drops

    def getSpinTypes(self):
        st = set()
        for event in self.getEvents():
            # print(event)
            for s in self.params_gacha.get(event).get("spin_types"):
               #  print(s)
                st.add(s.get('title'))
        st.add('ATLAS CHEST')
        st.add('ATLAS BADGE CHEST')
        st.add('SPECIAL CHEST')
        # st.add('EASTER CHEST')
        # st.add('SPOOKFEST CHEST')
        # print(st)
        return list(st)
