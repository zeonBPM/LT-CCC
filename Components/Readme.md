

Add new components in the corresponding folder with the component as a .py (phyton) file, and all dependencies as imports on top of it(if needed), as seen in the example file.



Try to have a detailed description of what the component does, assuming the name is not enough.








 If for some reason i forgot to add the dependencies, this are ALL the ones in the repo

```

from __future__ import annotations

import random

from app.data.database.components import ComponentType
from app.data.database.database import DB
from app.data.database.skill_components import SkillComponent, SkillTags

from app.engine import (action, banner, combat_calcs, engine, equations,
                        image_mods, item_funcs, item_system, skill_system,
                        target_system)
from app.engine.game_state import game
from app.engine.objects.unit import UnitObject
from app.engine.objects.region import RegionObject
from app.engine.skill_components import charge_components
from app.engine.combat import playback as pb
from app.engine.item_components.aoe_components import ShapeBlastAOE
from app.engine.movement import movement_funcs

from app.data.database.item_components import ItemComponent, ItemTags

from app.extensions.shape_dialog import rotate

from app.utilities import (utils, static_random)

```

