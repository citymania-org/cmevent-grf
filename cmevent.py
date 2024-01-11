import itertools
from typing import Optional, Union

from typeguard import typechecked

import grf

g = grf.NewGRF(
    grfid=b'CM\x01\x01',
    name='CityMania Special Events 1.5.1',
    description='Custom NewGRF for CityMania special events',
    url='https://github.com/citymania-org/cmevent-grf',
    min_compatible_version=5,
    version=5,
)

T1_SCALE = 3  # num of trains 8pax+4mail
T2_SCALE = 15  # approx num of trains
T3_SCALE = 15  # num of trains 4+4+4

g.add_int_parameter(name='T1 passenger requirement', description='', default=320 * T1_SCALE)
g.add_int_parameter(name='T1 mail requirement', description='', default=120 * T1_SCALE)
g.add_int_parameter(name='T2 every cargo requirement', description='', default=360 * (T2_SCALE // 3))
g.add_int_parameter(name='T3 sweets requirement', description='', default=100 * T3_SCALE)
g.add_int_parameter(name='T3 fizzy drinks requirement', description='', default=100 * T3_SCALE)
g.add_int_parameter(name='T3 toys requirement', description='', default=80 * T3_SCALE)

Industry = g.bind(grf.Industry)

g.add(grf.ReplaceOldSprites([(2072, 6)]))
png = grf.ImageFile("gfx/candyflossforest.png")
for x, y, w, h, xofs, yofs in [
        [  82,    8,  45,  66, -22, -40],
        [ 146,    8,  55,  66, -27, -40],
        [ 210,    8,  56,  66, -28, -40],
        [ 274,    8,  61,  66, -30, -40],
        [ 354,    8,  35,  66, -17, -40],
        [ 402,    8,  64,  31, -31,   0]]:
    g.add(grf.FileSprite(png, x, y, w, h, xofs=xofs, yofs=yofs))

png = grf.ImageFile("gfx/xmas_sprites.png")

g.add(grf.ReplaceOldSprites([(1768, 1)]))
g.add(grf.FileSprite(png, 10, 107, 25, 46, xofs=-15, yofs=-39))

g.add(grf.ReplaceOldSprites([(2601, 1)]))
g.add(grf.FileSprite(png, 123, 20, 64, 77, xofs=-31, yofs=-60))

BATT, BUBL, COLA, CTCD, PLST, SUGR, TOFF, SWET, FZDR, TOYS, PASS, MAIL = \
    g.set_cargo_table(['BATT', 'BUBL', 'COLA', 'CTCD', 'PLST', 'SUGR', 'TOFF', 'SWET', 'FZDR', 'TOYS', 'PASS', 'MAIL'])

RAIL, ELRL, MONO, MGLV, UNIV, WETR, UNI1 = \
    g.set_railtype_table(['RAIL', 'ELRL', 'MONO', 'MGLV', 'UNIV', 'WETR', 'UNI1'])

for i, l in ((1, b'RAIL'), (2, b'ELRL'), (3, b'MONO'), (4, b'MGLV'), (12, b'WETR')):
    g.add(grf.Define(
        feature=grf.RAILTYPE,
        id=i,
        props={
            'label': l,
            'construction_cost': 65000,
            'introduction_date': grf.Date(5000000, 12, 31),
        },
    ))

g.add(grf.DisableDefault(grf.TRAIN))

png = grf.ImageFile("gfx/xmas_tree00.png")
g.add(grf.Action1(
    feature=grf.HOUSE,
    set_count=1,
    sprite_count=4
))
for x, y, w, h, xofs, yofs in [
        [ 98, 8, 22, 46, -12, -34],
        [130, 8, 22, 46, -12, -34],
        [306, 8, 22, 46, -12, -34],
        [338, 8, 22, 46, -12, -34]]:
    g.add(grf.FileSprite(png, x, y, w, h, xofs=xofs, yofs=yofs))

tree_layout = grf.AdvancedSpriteLayout(
    feature=grf.HOUSE,
    ground={
        'sprite': grf.SpriteRef(0, is_global=True),
        'add': grf.Temp(0),
    },
    buildings=[{
        'sprite': grf.SpriteRef(0, is_global=False),
        'offset': (4, 4, 0),
        'extent': (8, 8, 45),
    }]
)

tree_switch = grf.Switch(
    'TEMP[0]=(terrain_type == 4) * 3130 + 1420', # 4550 if snow else 1420 (GROUNDSPRITE_CONCRETE)
    ranges={0: tree_layout},
    default=tree_layout,
)

TZ0, TZ1, TZ2, TZ3, TZ4 = 1, 2, 4, 8, 16
ARCTIC_ABOVE, TEMPERATE, ARCTIC_BELOW, TROPICAL, TOYLAND = 0x800, 0x1000, 0x2000, 0x4000, 0x8000
ALL_TOWN_ZONES = TZ0 | TZ1 | TZ2 | TZ3 | TZ4
ALL_CLIMATES = ARCTIC_ABOVE | TEMPERATE | ARCTIC_BELOW | TROPICAL | TOYLAND


g.add(definition := grf.Define(
    feature=grf.HOUSE,
    id=0,
    props={
        'substitute': 9,
        'flags': 3,
        'name': g.strings.add('Christmas Tree').get_global_id() + 0xD000,
        'population': 8,
        'mail_mult': 8,
        'tile_acceptance': [(g.get_cargo_id('PASS'), 8), (g.get_cargo_id('MAIL'), 8)],
        'authority_impact': 65525,
        'removal_cost_mult': 255,
        'probability': 16,
        'min_year': 1,
        'max_year': 9999,
        'min_life': 255,
        'availability_mask': ALL_CLIMATES | ALL_TOWN_ZONES,
    }
))

g.add(grf.Map(
    definition=definition,
    maps={},
    default=tree_switch,
))


# spriteset (spriteset_xmas_tree_1) {
#     [ 98, 8, 22, 46, -12, -34, "gfx/xmas_tree00.png"]
#     [130, 8, 22, 46, -12, -34, "gfx/xmas_tree00.png"]
#     [306, 8, 22, 46, -12, -34, "gfx/xmas_tree00.png"]
#     [338, 8, 22, 46, -12, -34, "gfx/xmas_tree00.png"]
# }

# item (FEAT_OBJECTS, xmas_tree_1) {
#     property {
#         class: "STRU";
#         classname: string(STR_XMAS_TREE_1);
#         name: string(STR_XMAS_TREE_1);
#         climates_available: ALL_CLIMATES;
#         size: [1,1];
#         build_cost_multiplier: 2;
#         remove_cost_multiplier: 8;
#         introduction_date: date(1,1,1);
#         end_of_life_date: 0xFFFFFFFF;
#         object_flags: bitmask(OBJ_FLAG_IRREMOVABLE, OBJ_FLAG_NO_FOUNDATIONS, OBJ_FLAG_ALLOW_BRIDGE);
#         height: 2;
#         num_views: 1;
#     }
#     graphics {
#         default: spritelayout_xmas_tree_1;
#         additional_text: string(STR_XMAS_TREE_1);
#     }
# }

g.add(grf.DisableDefault(grf.CARGO, [1] + list(range(3, 30))))


def add_cargo(id, **props):
    g.add(grf.Define(
        feature=grf.CARGO,
        id=id,
        props={
           'town_growth_multiplier': 0,
           'is_freight': 1,
            **props
        }
    ))

add_cargo(
    id=1,
    label=b'SUGR',
    type_name=grf.TTDString.CARGO_PLURAL_SUGAR,
    unit_name=grf.TTDString.CARGO_SINGULAR_SUGAR,
    type_abbreviation=grf.TTDString.ABBREV_SUGAR,
    units_of_cargo=grf.TTDString.TONS,
    items_of_cargo=grf.TTDString.QUANTITY_SUGAR,
    cargo_payment_list_colour=6,
    station_list_colour=6,
    weight=16,
    town_growth_effect=grf.TownGrowthEffect.NONE,
    single_penalty_length=255,
    icon_sprite=4316,
    cargo_classes=grf.CargoClass.BULK,
    penalty_lowerbound=20,
    base_price=4437,
    capacity_multiplier=256,
    bit_number=1,
)

add_cargo(
    id=3,
    label=b'TOYS',
    units_of_cargo=grf.TTDString.ITEMS,
    cargo_payment_list_colour=174,
    weight=2,
    town_growth_effect=grf.TownGrowthEffect.NONE,
    single_penalty_length=255,
    items_of_cargo=grf.TTDString.QUANTITY_TOYS,
    icon_sprite=4317,
    unit_name=grf.TTDString.CARGO_SINGULAR_TOY,
    type_abbreviation=grf.TTDString.ABBREV_TOYS,
    cargo_classes=grf.CargoClass.PIECE_GOODS,
    penalty_lowerbound=25,
    type_name=grf.TTDString.CARGO_PLURAL_TOYS,
    base_price=5574,
    capacity_multiplier=256,
    bit_number=3,
    station_list_colour=174,
)

add_cargo(
    id=4,
    label=b'BATT',
    units_of_cargo=grf.TTDString.ITEMS,
    cargo_payment_list_colour=208,
    weight=4,
    town_growth_effect=grf.TownGrowthEffect.NONE,
    single_penalty_length=30,
    items_of_cargo=grf.TTDString.QUANTITY_BATTERIES,
    icon_sprite=4323,
    unit_name=grf.TTDString.CARGO_SINGULAR_BATTERY,
    type_abbreviation=grf.TTDString.ABBREV_BATTERIES,
    cargo_classes=grf.CargoClass.PIECE_GOODS,
    penalty_lowerbound=2,
    type_name=grf.TTDString.CARGO_PLURAL_BATTERIES,
    base_price=4322,
    capacity_multiplier=256,
    bit_number=4,
    station_list_colour=208,
)

add_cargo(
    id=5,
    label=b'SWET',
    units_of_cargo=grf.TTDString.BAGS,
    cargo_payment_list_colour=194,
    weight=5,
    town_growth_effect=grf.TownGrowthEffect.GOODS,
    single_penalty_length=40,
    items_of_cargo=grf.TTDString.QUANTITY_SWEETS,
    icon_sprite=4315,
    unit_name=grf.TTDString.CARGO_SINGULAR_SWEETS,
    type_abbreviation=grf.TTDString.ABBREV_SWEETS,
    cargo_classes=grf.CargoClass.EXPRESS,
    penalty_lowerbound=8,
    type_name=grf.TTDString.CARGO_PLURAL_SWEETS,
    base_price=6144,
    capacity_multiplier=512,
    bit_number=5,
    station_list_colour=194,
)

add_cargo(
    id=6,
    label=b'TOFF',
    units_of_cargo=grf.TTDString.TONS,
    cargo_payment_list_colour=191,
    weight=16,
    town_growth_effect=grf.TownGrowthEffect.NONE,
    single_penalty_length=60,
    items_of_cargo=grf.TTDString.QUANTITY_TOFFEE,
    icon_sprite=4320,
    unit_name=grf.TTDString.CARGO_SINGULAR_TOFFEE,
    type_abbreviation=grf.TTDString.ABBREV_TOFFEE,
    cargo_classes=grf.CargoClass.BULK,
    penalty_lowerbound=14,
    type_name=grf.TTDString.CARGO_PLURAL_TOFFEE,
    base_price=4778,
    capacity_multiplier=256,
    bit_number=6,
    station_list_colour=191,
)

add_cargo(
    id=7,
    label=b'COLA',
    units_of_cargo=grf.TTDString.LITERS,
    cargo_payment_list_colour=84,
    weight=16,
    town_growth_effect=grf.TownGrowthEffect.NONE,
    single_penalty_length=75,
    items_of_cargo=grf.TTDString.QUANTITY_COLA,
    icon_sprite=4310,
    unit_name=grf.TTDString.CARGO_SINGULAR_COLA,
    type_abbreviation=grf.TTDString.ABBREV_COLA,
    cargo_classes=grf.CargoClass.LIQUID,
    penalty_lowerbound=5,
    type_name=grf.TTDString.CARGO_PLURAL_COLA,
    base_price=4892,
    capacity_multiplier=256,
    bit_number=7,
    station_list_colour=84,
)

add_cargo(
    id=8,
    label=b'CTCD',
    units_of_cargo=grf.TTDString.TONS,
    cargo_payment_list_colour=184,
    weight=16,
    town_growth_effect=grf.TownGrowthEffect.NONE,
    single_penalty_length=25,
    items_of_cargo=grf.TTDString.QUANTITY_CANDYFLOSS,
    icon_sprite=4318,
    unit_name=grf.TTDString.CARGO_SINGULAR_CANDYFLOSS,
    type_abbreviation=grf.TTDString.ABBREV_CANDYFLOSS,
    cargo_classes=grf.CargoClass.BULK,
    penalty_lowerbound=10,
    type_name=grf.TTDString.CARGO_PLURAL_CANDYFLOSS,
    base_price=5005,
    capacity_multiplier=256,
    bit_number=8,
    station_list_colour=184,
)

add_cargo(
    id=9,
    label=b'BUBL',
    units_of_cargo=grf.TTDString.ITEMS,
    cargo_payment_list_colour=10,
    weight=1,
    town_growth_effect=grf.TownGrowthEffect.NONE,
    single_penalty_length=80,
    items_of_cargo=grf.TTDString.QUANTITY_BUBBLES,
    icon_sprite=4321,
    unit_name=grf.TTDString.CARGO_SINGULAR_BUBBLE,
    type_abbreviation=grf.TTDString.ABBREV_BUBBLES,
    cargo_classes=grf.CargoClass.PIECE_GOODS,
    penalty_lowerbound=20,
    type_name=grf.TTDString.CARGO_PLURAL_BUBBLES,
    base_price=5077,
    capacity_multiplier=256,
    bit_number=9,
    station_list_colour=10,
)

add_cargo(
    id=10,
    label=b'PLST',
    units_of_cargo=grf.TTDString.LITERS,
    cargo_payment_list_colour=202,
    weight=16,
    town_growth_effect=grf.TownGrowthEffect.NONE,
    single_penalty_length=255,
    items_of_cargo=grf.TTDString.QUANTITY_PLASTIC,
    icon_sprite=4322,
    unit_name=grf.TTDString.CARGO_SINGULAR_PLASTIC,
    type_abbreviation=grf.TTDString.ABBREV_PLASTIC,
    cargo_classes=grf.CargoClass.LIQUID,
    penalty_lowerbound=30,
    type_name=grf.TTDString.CARGO_PLURAL_PLASTIC,
    base_price=4664,
    capacity_multiplier=256,
    bit_number=10,
    station_list_colour=202,
)

add_cargo(
    id=11,
    label=b'FZDR',
    units_of_cargo=grf.TTDString.ITEMS,
    cargo_payment_list_colour=48,
    weight=2,
    town_growth_effect=grf.TownGrowthEffect.FOOD,
    single_penalty_length=50,
    items_of_cargo=grf.TTDString.QUANTITY_FIZZY_DRINKS,
    icon_sprite=4319,
    unit_name=grf.TTDString.CARGO_SINGULAR_FIZZY_DRINK,
    type_abbreviation=grf.TTDString.ABBREV_FIZZY_DRINKS,
    cargo_classes=grf.CargoClass.PIECE_GOODS,
    penalty_lowerbound=30,
    type_name=grf.TTDString.CARGO_PLURAL_FIZZY_DRINKS,
    base_price=6250,
    capacity_multiplier=256,
    bit_number=11,
    station_list_colour=48,
)

# /*

# spriteset(oilwell_ground_overlay, "src/gfx/oil_wells/oil_wells.png") {
#     tmpl_level_ground(7,9)
# }

# spritelayout oil_wells_tile_construction {
#     ground { sprite: GROUNDSPRITE_CLEARED; }
# }

# GROUND_AWARE_SPRITELAYOUT(oil_wells_tile(sprite_offset))
#     GROUND_SPRITE_OVERLAY(oilwell_ground_overlay)
#     CONDITIONAL_BUILDING_SPRITE(2174 + sprite_offset, 32, 1)
# SPRITELAYOUT_END

# /* We use animation frames 1..10 for the continued animation as a loop
#  * frames 11 .. 20 are the same animation frames, but animation will stop at frame 11
#  * this is needed so the last cycle can be finished gracefully
#  */ /*
# switch (FEAT_INDUSTRYTILES, SELF, oil_wells_tile_animation, animation_frame) {
#     2:  oil_wells_tile(1);
#     3:  oil_wells_tile(2);
#     4:  oil_wells_tile(3);
#     5:  oil_wells_tile(4);
#     6:  oil_wells_tile(5);
#     7:  oil_wells_tile(4);
#     8:  oil_wells_tile(3);
#     9:  oil_wells_tile(2);
#     10: oil_wells_tile(1);
#     12: oil_wells_tile(1);
#     13: oil_wells_tile(2);
#     14: oil_wells_tile(3);
#     15: oil_wells_tile(4);
#     16: oil_wells_tile(5);
#     17: oil_wells_tile(4);
#     18: oil_wells_tile(3);
#     19: oil_wells_tile(2);
#     20: oil_wells_tile(1);
#     oil_wells_tile(0);
# }


# switch (FEAT_INDUSTRYTILES, SELF, oil_wells_tile_1_stop_anim, animation_frame) {
#     1: return 11; // jump to the 'stop animation cycle' when triggered and currently animated
#     2: return 12;
#     3: return 13;
#     4: return 14;
#     5: return 15;
#     6: return 16;
#     7: return 17;
#     8: return 18;
#     9: return 19;
#     10: return 20;
#     return CB_RESULT_DO_NOTHING;
# }

# switch (FEAT_INDUSTRYTILES, SELF, oil_wells_tile_1_start_anim, animation_frame) {
#     11: return 1;
#     12: return 2;
#     13: return 3;
#     14: return 4;
#     15: return 5;
#     16: return 6;
#     17: return 7;
#     18: return 8;
#     19: return 9;
#     20: return 10;
#     return CB_RESULT_START_ANIMATION;
# }
# random_switch (FEAT_INDUSTRYTILES, SELF, oil_wells_tile_1_random_anim_trigger_switch, bitmask(TRIGGER_INDUSTRYTILE_TILELOOP)) {
#     1: return oil_wells_tile_1_stop_anim;
#     1: return oil_wells_tile_1_start_anim;
# }

# switch (FEAT_INDUSTRYTILES, SELF, oil_wells_tile_1_next_frame_switch, animation_frame) {
#     10: return 1;
#     11: return CB_RESULT_STOP_ANIMATION; // Don't actually stop animation, just keep looping the same frame over and over. // CB_RESULT_STOP_ANIMATION
#     20: return 11;
#     return CB_RESULT_NEXT_FRAME;
# }

# switch (FEAT_INDUSTRYTILES, SELF, oil_wells_tile_1_graphics_switch, construction_state) {
#     0: oil_wells_tile_construction;
#     1: oil_wells_tile(0);
#     2: oil_wells_tile(0);
#     oil_wells_tile_animation;
# }

# item(FEAT_INDUSTRYTILES, oil_wells_tile_1) {
#     property {
#         substitute:         0x1D;
#         override:           0x1D;
#         animation_info:     [ANIMATION_LOOPING, 20];
#         animation_speed:    3;
#         animation_triggers: bitmask(ANIM_TRIGGER_INDTILE_TILE_LOOP);
#         special_flags:      bitmask(INDTILE_FLAG_RANDOM_ANIMATION);
#     }
#     graphics {
#         anim_control: oil_wells_tile_1_random_anim_trigger_switch;
#         anim_next_frame: oil_wells_tile_1_next_frame_switch;
#         random_trigger: oil_wells_tile_1_random_anim_trigger_switch;
#         oil_wells_tile_1_graphics_switch;
#     }
# }

# spritelayout spritelayout_xmas_tree_1 {
#     ground {
#         sprite: GROUNDSPRITE_CONCRETE;
#     }
#     childsprite {
#         sprite: spriteset_xmas_tree_1(0);
#     }
# }

# GROUND_AWARE_SPRITELAYOUT(oil_wells_tile(sprite_offset))
#     GROUND_SPRITE_OVERLAY(oilwell_ground_overlay)
#     CONDITIONAL_BUILDING_SPRITE(2174 + sprite_offset, 32, 1)
# SPRITELAYOUT_END

# */

g.add(grf.DisableDefault(grf.INDUSTRY, range(0x24)))


def add_industry(substitute_type, **props):
    for k in ('production_types', 'acceptance_types'):
        if k in props:
            props[k] = [g.get_cargo_id(x) for x in props[k]]

    props['ingame_probability'] = 1
    props['mapgen_probability'] = 0
    g.add(grf.Define(
        id=substitute_type,
        feature=grf.INDUSTRY,
        props={
            'substitute_type': substitute_type,
            **props
        }
    ))


add_industry(
    substitute_type=grf.TTDIndustry.CANDYFLOSS_FOREST,
    mapgen_probability=5,
    ingame_probability=3,
    production_types=['CTCD'],
)

add_industry(
    substitute_type=grf.TTDIndustry.SUGAR_MINE,
    ingame_probability=2,
    mapgen_probability=4,
    production_types=['SUGR'],
)

add_industry(
    substitute_type=grf.TTDIndustry.TOFFE_QUARRY,
    ingame_probability=3,
    mapgen_probability=5,
    production_types=['TOFF'],
)

add_industry(
    substitute_type=grf.TTDIndustry.SWEETS_FACTORY,
    ingame_probability=3,
    mapgen_probability=5,
    acceptance_types=['TOFF', 'CTCD', 'SUGR'],
    production_types=['SWET'],
)

add_industry(
    substitute_type=grf.TTDIndustry.COLA_WELLS,
    ingame_probability=3,
    mapgen_probability=5,
    production_types=['COLA'],
)

add_industry(
    substitute_type=grf.TTDIndustry.BUBBLE_GENERATOR,
    ingame_probability=3,
    mapgen_probability=5,
    production_types=['BUBL'],
)

add_industry(
    substitute_type=grf.TTDIndustry.FIZZY_DRINKS_FACTORY,
    ingame_probability=3,
    mapgen_probability=4,
    acceptance_types=['COLA', 'BUBL'],
    production_types=['FZDR'],
)

add_industry(
    substitute_type=grf.TTDIndustry.PLASTIC_FOUNTAIN,
    ingame_probability=3,
    mapgen_probability=5,
    production_types=['PLST'],
)

add_industry(
    substitute_type=grf.TTDIndustry.BATTERY_FARM,
    ingame_probability=3,
    mapgen_probability=4,
    production_types=['BATT'],
)

add_industry(
    substitute_type=grf.TTDIndustry.TOY_FACTORY,
    ingame_probability=3,
    mapgen_probability=5,
    acceptance_types=['PLST', 'BATT'],
    production_types=['TOYS'],
)

add_industry(
    substitute_type=grf.TTDIndustry.TOY_SHOP,
    ingame_probability=3,
    mapgen_probability=4,
    acceptance_types=['TOYS'],
    special_flags=0,
)


def add_gift_industry(tier, image, z_extent, **props):
    img = grf.ImageFile(image)
    sprite = grf.FileSprite(img, 1, 1, 256, 282, xofs=-127, yofs=-251)

    ind = Industry(
        id=f'gift_box_{tier}',
        substitute_type=0,
        name=f'Gift (Tier {tier})',
        layouts=[
            [(0, 0, Industry.Building(size=(4, 4), sprite=sprite))],
        ],
        z_extent=z_extent,
        ground_sprite_id=1420,
        production_types=[],
        cb_flags=0x4,  # enable storage by using production callback flag (no callback itself though)
        special_flags=0x10000 | 0x20000,
        fund_cost=0xff,
        **props,
    )

    ind.callbacks.input_cargo = grf.Eval(
        'PERM[extra_callback_info1_byte]',
        default=0xFF,
    )

    ind.callbacks.cargo_subtype_display = grf.Switch(
        f'''
            cargonum = extra_callback_info2 & 0xFF
            TEMP[0x100] = var(0x6f, param=PERM[cargonum], shift=0, and=0xFFFFFFFF)
            TEMP[0x101] = PERM[cargonum + 4]
            extra_callback_info2
        ''',
        ranges={
            (0x100 | 0, 0x100 | 2): g.strings.add(' ({COMMA}/{COMMA})').get_global_id() | 0x800,
        },
        default=0x401,
    )

    ind.tile_callbacks.tile_check = grf.Switch(
        'var(0x60, param=0, shift=0, and=0xFF)',
        ranges= {0: 0x400},  # only allow flat tiles so everything is flat
        default = 0x401,
    )

    return ind

t1 = add_gift_industry(
    tier=1,
    image="gfx/gift_box.png",
    z_extent=154,
    acceptance_types=['PASS', 'MAIL'],
    map_colour=0xB7,
)

t1.callbacks.init_production = grf.Eval(
    f'''
        PERM[0] = {PASS}
        PERM[1] = {MAIL}
        PERM[2] = 0xFF
        PERM[3] = 0xFF
        PERM[4] = var(0x7f, param=0, shift=0, and=0xFFFFFFFF)
        PERM[5] = var(0x7f, param=1, shift=0, and=0xFFFFFFFF)
        PERM[6] = 0
        16
    ''', # 1000 225
    default=16,
)

# require 3 out of BATT, BUBL, COLA, CTCD, PLST, SUGR, TOFF,
t2 = add_gift_industry(
    tier=2,
    image="gfx/gift_box2.png",
    z_extent=150,
    acceptance_types=['BATT', 'BUBL', 'COLA', 'CTCD', 'PLST', 'SUGR', 'TOFF'],
    map_colour=0xAA,
)

t2.callbacks.init_production = grf.Eval(
    f'''
        combination = gen_cargo_combination()
        PERM[0] = combination >> 8
        PERM[1] = (combination >> 4) & 15
        PERM[2] = combination & 15
        PERM[3] = 0xFF
        PERM[4] = var(0x7f, param=2, shift=0, and=0xFFFFFFFF)
        PERM[5] = PERM[4]
        PERM[6] = PERM[4]
        16
    ''',
    default=16,
    subroutines={
        'gen_cargo_combination': grf.Switch(
            code='random_bits % 35',
            ranges={i:(a << 8) | (b << 4) | c for i,(a, b, c) in enumerate(itertools.combinations(range(7), 3))},
            default=(1 << 4) | 2,
        )
    }
)

# require all TOYS, FZDR, SWET
t3 = add_gift_industry(
    tier=3,
    image="gfx/gift_box3.png",
    z_extent=150,
    acceptance_types=['SWET', 'FZDR', 'TOYS'],
    map_colour=0x95,
)

t3.callbacks.init_production = grf.Eval(
    f'''
        PERM[0] = {SWET}
        PERM[1] = {FZDR}
        PERM[2] = {TOYS}
        PERM[3] = 0xFF
        PERM[4] = var(0x7f, param=3, shift=0, and=0xFFFFFFFF)
        PERM[5] = var(0x7f, param=4, shift=0, and=0xFFFFFFFF)
        PERM[6] = var(0x7f, param=5, shift=0, and=0xFFFFFFFF)
        16
    ''',
    default=16,
)

grf.main(g, 'cmevent.grf')
