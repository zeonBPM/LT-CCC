def create_unit_info(self, unit):
        font = FONT['info-grey']
        font2 = FONT['number_small']
        dimensions = (112, 77)
        width, height = dimensions
        surf = SPRITES.get('unit_info_bg').copy()
        top, left = 4, 6
        if not unit.portrait_nid and unit.faction:
            icons.draw_faction(surf, DB.factions.get(unit.faction), (left + 1, top + 4))
        elif unit.portrait_nid:
            surf = SPRITES.get('unit_info_bg').copy()
            portrait_nid = unit.portrait_nid
            icons.draw_chibi(surf, portrait_nid, (left + 1, top + 4))

        # # Health BG
        current_hp = unit.get_hp()
        max_hp = equations.parser.hitpoints(unit)

        # Health text
        surf.blit(SPRITES.get('unit_info_hp'), (left + 34, top + 27))
        surf.blit(SPRITES.get('unit_info_slash'), (left + 68, top + 28))

        font.blit_right(str(current_hp), surf, (left + 66, top + 23))
        font.blit_right(str(max_hp), surf, (left + 90, top + 23))

        # Level text
        surf.blit(SPRITES.get('lv_sprite'), (left + 34, top + 18))
        surf.blit(SPRITES.get('exp_sprite'), (left + 68, top + 18))
        lvl = unit.level
        exper = unit.exp
        font.blit_right(str(lvl), surf, (left + 66, top + 14))
        font.blit_right(str(exper), surf, (left + 90, top + 14))


        # Weapon Icon
        itNum = 0
        for item in unit.items:
            icon = icons.get_icon(item) 
            if icon:
                pos = (left + (itNum) * 16, top + 51)
                surf.blit(icon, pos)
                itNum += 1

        # Combat stats
        atk = "--"
        atk_spd = "--"
        hit = "--"
        crit = "--"
        prt = str(unit.get_stat('DEF'))
        rsl = str(unit.get_stat('RES'))

        left += 2
        if unit.get_weapon():
            atk = combat_calcs.damage(unit, unit.get_weapon())
            hit = combat_calcs.accuracy(unit, unit.get_weapon())
            crit = combat_calcs.crit_accuracy(unit, unit.get_weapon())
            atk_spd = combat_calcs.attack_speed(unit, unit.get_weapon())
        
        #Top Row
        surf.blit(SPRITES.get('atk_sprite'), (left, top + 36))
        font.blit_right(str(atk), surf, (left + 28, top + 31))

        surf.blit(SPRITES.get('def_sprite'), (left + 28, top + 36))
        font.blit_right(prt, surf, (left + 57, top + 31))

        surf.blit(SPRITES.get('hit_sprite'), (left + 57, top + 36))
        font.blit_right(str(hit), surf, (left + 90, top + 31))
        

        #Bottom Row
        surf.blit(SPRITES.get('as_sprite'), (left, top + 44))
        font.blit_right(str(atk_spd), surf, (left + 28, top + 39))

        surf.blit(SPRITES.get('res_sprite'), (left + 28, top + 44))
        font.blit_right(rsl, surf, (left + 57, top + 39))

        surf.blit(SPRITES.get('crt_sprite'), (left + 57, top + 44))
        font.blit_right(str(crit), surf, (left + 90, top + 39))

        # Name
        name = unit.name
        pos = (left + 47, top + 4)
        if unit.generic:
            short_name = DB.classes.get(unit.klass).name
        font.blit(name, surf, pos)
        return surf