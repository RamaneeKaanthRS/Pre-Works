import json
import os
from datetime import datetime
try:
    from reportlab.lib.pagesizes import A4, portrait
    from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
    from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle, PageBreak
    from reportlab.lib import colors
    from reportlab.lib.units import mm
except Exception:
    reportlab = None

PROJECT_EXT = ".fpproj"

class Character:
    def __init__(self, name, age, characteristics, movie, most_used_hand):
        self.name = name
        self.age = age
        self.characteristics = characteristics
        self.movie = movie
        self.most_used_hand = most_used_hand
    def to_dict(self):
        return self.__dict__
    @staticmethod
    def from_dict(d):
        return Character(d.get('name',''), d.get('age',''), d.get('characteristics',''), d.get('movie',''), d.get('most_used_hand',''))

class Shot:
    def __init__(self, title='', description='', camera='', focal_length='', aperture='', shutter='', iso='', lens='', movement='', duration=''):
        self.title = title
        self.description = description
        self.camera = camera
        self.focal_length = focal_length
        self.aperture = aperture
        self.shutter = shutter
        self.iso = iso
        self.lens = lens
        self.movement = movement
        self.duration = duration
    def to_dict(self):
        return self.__dict__
    @staticmethod
    def from_dict(d):
        return Shot(**d)

class Project:
    def __init__(self):
        self.title = 'Untitled'
        self.author = ''
        self.date = datetime.now().strftime('%Y-%m-%d')
        self.story = ''
        self.screenplay = ''
        self.characters = []
        self.shots = []
    def to_dict(self):
        return {'title':self.title,'author':self.author,'date':self.date,'story':self.story,'screenplay':self.screenplay,'characters':[c.to_dict() for c in self.characters],'shots':[s.to_dict() for s in self.shots]}
    @staticmethod
    def from_dict(d):
        p = Project()
        p.title = d.get('title','Untitled')
        p.author = d.get('author','')
        p.date = d.get('date',datetime.now().strftime('%Y-%m-%d'))
        p.story = d.get('story','')
        p.screenplay = d.get('screenplay','')
        p.characters = [Character.from_dict(cd) for cd in d.get('characters',[])]
        p.shots = [Shot.from_dict(sd) for sd in d.get('shots',[])]
        return p

def format_screenplay(text):
    lines = text.splitlines()
    out = []
    prev = ''
    for ln in lines:
        s = ln.strip()
        if not s:
            out.append({'t':'sp','v':''}); prev = ''
            continue
        up = s.upper()
        if up.startswith(('INT.','EXT.','SCENE')):
            out.append({'t':'scene','v':up}); prev = 'scene'; continue
        if s.isupper() and len(s.split())<=4:
            out.append({'t':'char','v':s}); prev='char'; continue
        if s.startswith('(') and s.endswith(')'):
            out.append({'t':'paren','v':s}); prev='paren'; continue
        if prev=='char':
            out.append({'t':'dlg','v':s}); prev='dlg'; continue
        out.append({'t':'action','v':s}); prev='action'
    return out

def export_pdf(project, path):
    if 'reportlab' not in globals() or reportlab is None:
        raise RuntimeError('Install reportlab to export PDF: pip install reportlab')
    doc = SimpleDocTemplate(path, pagesize=portrait(A4), rightMargin=20*mm, leftMargin=20*mm, topMargin=18*mm, bottomMargin=18*mm)
    styles = getSampleStyleSheet()
    elems = []
    elems.append(Paragraph(project.title, ParagraphStyle('T', parent=styles['Title'], alignment=1)))
    elems.append(Paragraph(f"Author: {project.author}", styles['Normal']))
    elems.append(Paragraph(f"Date: {project.date}", styles['Normal']))
    elems.append(Spacer(1,12))
    elems.append(Paragraph('Story', styles['Heading3']))
    for p in project.story.split('

'):
        elems.append(Paragraph(p.replace('
',' '), styles['Normal']))
        elems.append(Spacer(1,6))
    elems.append(PageBreak())
    elems.append(Paragraph('Screenplay', styles['Heading3']))
    for item in format_screenplay(project.screenplay):
        t = item['v']
        if item['t']=='scene':
            elems.append(Paragraph(t, ParagraphStyle('S', parent=styles['Heading4'])))
        elif item['t']=='char':
            elems.append(Paragraph(t, ParagraphStyle('C', parent=styles['Normal'], alignment=1, fontName='Helvetica-Bold')))
        elif item['t']=='dlg':
            elems.append(Paragraph(t, ParagraphStyle('D', parent=styles['Normal'], leftIndent=30, rightIndent=30)))
        elif item['t']=='paren':
            elems.append(Paragraph(t, ParagraphStyle('P', parent=styles['Normal'], leftIndent=50, rightIndent=50, italic=True)))
        else:
            elems.append(Paragraph(t, styles['Normal']))
    elems.append(PageBreak())
    elems.append(Paragraph('Characters', styles['Heading3']))
    if project.characters:
        data = [['Name','Age','Characteristics','Movie','Hand']]
        for c in project.characters:
            data.append([c.name,str(c.age),c.characteristics,c.movie,c.most_used_hand])
        tbl = Table(data, colWidths=[60*mm,20*mm,60*mm,40*mm,20*mm])
        tbl.setStyle(TableStyle([('GRID',(0,0),(-1,-1),0.3,colors.black),('BACKGROUND',(0,0),(-1,0),colors.grey),('TEXTCOLOR',(0,0),(-1,0),colors.whitesmoke)]))
        elems.append(tbl)
    else:
        elems.append(Paragraph('No characters', styles['Normal']))
    elems.append(PageBreak())
    elems.append(Paragraph('Shots', styles['Heading3']))
    if project.shots:
        for i,s in enumerate(project.shots,1):
            elems.append(Paragraph(f"{i}. {s.title}", styles['Heading4']))
            shot_data = [['Camera',s.camera,'Lens',s.lens],['Focal',s.focal_length,'Aperture',s.aperture],['Shutter',s.shutter,'ISO',s.iso],['Movement',s.movement,'Duration',s.duration]]
            st = Table(shot_data, colWidths=[30*mm,60*mm,30*mm,60*mm])
            st.setStyle(TableStyle([('GRID',(0,0),(-1,-1),0.3,colors.black)]))
            elems.append(st)
            elems.append(Paragraph(s.description or '-', styles['Normal']))
            elems.append(Spacer(1,6))
    else:
        elems.append(Paragraph('No shots', styles['Normal']))
    doc.build(elems)

def input_nonempty(prompt):
    while True:
        v = input(prompt).strip()
        if v:
            return v

def add_character_cli(project):
    name = input_nonempty('Name: ')
    age = input('Age: ').strip()
    characteristics = input('Characteristics: ').strip()
    movie = input('Movie: ').strip()
    hand = input('Most-used hand (Right/Left/Ambidextrous): ').strip()
    project.characters.append(Character(name, age, characteristics, movie, hand))
    print('Saved')

def list_characters(project):
    if not project.characters:
        print('No characters')
        return
    for i,c in enumerate(project.characters,1):
        print(i, c.name, c.age, '-', c.characteristics)

def delete_character_cli(project):
    list_characters(project)
    idx = input('Delete which number (blank to cancel): ').strip()
    if not idx:
        return
    try:
        i = int(idx)-1
        project.characters.pop(i)
        print('Deleted')
    except Exception:
        print('Invalid')

def add_shot_cli(project):
    title = input('Shot title: ').strip() or 'Shot'
    camera = input('Camera: ').strip()
    lens = input('Lens: ').strip()
    focal = input('Focal length: ').strip()
    aperture = input('Aperture: ').strip()
    shutter = input('Shutter: ').strip()
    iso = input('ISO: ').strip()
    movement = input('Movement: ').strip()
    duration = input('Duration: ').strip()
    desc = input('Description: ').strip()
    project.shots.append(Shot(title, desc, camera, focal, aperture, shutter, iso, lens, movement, duration))
    print('Saved')

def list_shots(project):
    if not project.shots:
        print('No shots')
        return
    for i,s in enumerate(project.shots,1):
        print(i, s.title, '-', s.camera, s.lens)

def delete_shot_cli(project):
    list_shots(project)
    idx = input('Delete which number (blank to cancel): ').strip()
    if not idx:
        return
    try:
        i = int(idx)-1
        project.shots.pop(i)
        print('Deleted')
    except Exception:
        print('Invalid')

def save_project(project, path):
    with open(path,'w',encoding='utf-8') as f:
        json.dump(project.to_dict(), f, indent=2, ensure_ascii=False)
    print('Saved to', path)

def load_project(path):
    with open(path,'r',encoding='utf-8') as f:
        data = json.load(f)
    return Project.from_dict(data)

def edit_story(project):
    print('Enter story. End with a line containing only . on its own')
    lines = []
    while True:
        l = input()
        if l.strip()=='.':
            break
        lines.append(l)
    project.story = '
'.join(lines)
    print('Story saved')

def edit_screenplay(project):
    print('Enter screenplay. End with a line containing only . on its own')
    lines = []
    while True:
        l = input()
        if l.strip()=='.':
            break
        lines.append(l)
    project.screenplay = '
'.join(lines)
    print('Screenplay saved')

def main():
    project = Project()
    path = ''
    while True:
        print('
Film Preproduction —', project.title)
        print('1) Edit metadata 2) Edit story 3) Edit screenplay 4) Characters 5) Shots 6) Save 7) Load 8) Export PDF 9) Quit')
        choice = input('Choose: ').strip()
        if choice=='1':
            project.title = input('Title: ').strip() or project.title
            project.author = input('Author: ').strip() or project.author
            print('Saved')
        elif choice=='2':
            edit_story(project)
        elif choice=='3':
            edit_screenplay(project)
        elif choice=='4':
            print('a) Add b) List c) Delete d) Back')
            c = input('> ').strip().lower()
            if c=='a': add_character_cli(project)
            elif c=='b': list_characters(project)
            elif c=='c': delete_character_cli(project)
        elif choice=='5':
            print('a) Add b) List c) Delete d) Back')
            c = input('> ').strip().lower()
            if c=='a': add_shot_cli(project)
            elif c=='b': list_shots(project)
            elif c=='c': delete_shot_cli(project)
        elif choice=='6':
            p = input('Save file path (.fpproj recommended): ').strip() or path or 'project'+PROJECT_EXT
            save_project(project, p)
            path = p
        elif choice=='7':
            p = input('Load file path: ').strip()
            if os.path.exists(p):
                project = load_project(p); path = p
                print('Loaded')
            else:
                print('Not found')
        elif choice=='8':
            p = input('Export PDF path: ').strip() or 'export.pdf'
            try:
                export_pdf(project, p)
                print('Exported to', p)
            except Exception as e:
                print('PDF export failed:', e)
        elif choice=='9':
            print('Bye')
            break
        else:
            print('Unknown')

if __name__=='__main__':
    main()
