RELATION_MAP = {
    'dad': ('👨', 'Dad'),
    'mom': ('👩', 'Mom'),
    'grandfather': ('👴', 'Grandfather'),
    'grandmother': ('👵', 'Grandmother'),
    'uncle': ('👨‍🦳', 'Uncle'),
    'aunty': ('👩‍🦳', 'Aunty'),
    'bro': ('🧑', 'Brother'),
    'sis': ('👧', 'Sister'),
    'wife': ('💍', 'Wife'),
    'gf': ('❤️', 'Girlfriend'),
    'crush': ('😍', 'Crush'),
    'son': ('👶', 'Son'),
    'daughter': ('👧', 'Daughter'),
    'motherinlaw': ('👵', 'Mother-in-Law'),
    'fatherinlaw': ('👴', 'Father-in-Law'),
    'saali': ('💃', 'Saali'),
    'ziza': ('😎', 'Ziza'),
    'friend': ('🤝', 'Friend'),
    'enemy': ('😈', 'Enemy'),
}

def format_tree_text(family_data):
    if not family_data:
        return "🍃 Your family tree is empty.\nReply to someone and use commands to start planting!"
    
    text = "╔═══ 🌳 YOUR FAMILY TREE 🌳 ═══╗\n\n"
    
    for row in family_data:
        rel_type = row['relation_type']
        fname = row['first_name']
        uname = row['username']
        
        if rel_type in RELATION_MAP:
            icon, title = RELATION_MAP[rel_type]
            display_name = f"@{uname}" if uname else fname
            text += f"{icon} {title}\n└── {display_name}\n\n"
    
    text += "━━━━━━━━━━━━━━━━━━━\n👑 FamilyTree Bot"
    return text
