# -*- coding: utf-8 -*-
import reportng
import os

os.mkdir('dtest')

reportng.Assets.download(download_path='./dtest', rel_path='./dtest', theme='pulse')
print('download_assets')


r = reportng.ReportWriter(report_name='somename', brand='somebrand',
                          asciinema=True, code=True, pbar=True)
report = r.report_header(script='alert(123);')
print('report_header')
content = """
    # fasfdds
    # fdsfsfsd
    # fdsfasdfsd
    # fdsfsdf
    # Malmö
    # 아름다운
    # 你好""" * 100
report += r.report_section(title='title', content=content, pre_tag=True,
                           tag_color='red', title_color=False, alert=('green', 'some message here'),
                           overflow='', badge={'red': 'red badge'}, reference=('green', 'https://google.com'))
print('report_section1')
report += r.report_section(title='title', content=content, pre_tag=True,
                           tag_color='danger', title_color=False, overflow='')
print('report_section2')
report += r.report_image_carousel('a', 'b', a='a', b='b')
print('report_image')
report += r.report_asciinema('https://asciinema.org/a/123683', title='title',
                             alert=('green', 'some message here'))
print('report_asciinema')
report += r.report_code_section(title='title', code="""
    $(document).ready(function() {
    $('pre code').each(function(i, block) {
        hljs.highlightBlock(block);
    });
    });)""", alert=('green', 'some message here'))
print('report_code')
report += r.report_captions('test')
print('report_captions')
report += r.report_table(
    ('a data', 'b data', 'c data', 'e data', 'f data', 'e data', 'f data', 'e data', 'f data', 'e data', 'f data'),
    ('a data', 'b data', 'c data', 'e data', 'f data', 'e data', 'f data', 'e data', 'f data', 'e data', 'f data'),
    ('a data', 'b data', 'c data', 'e data', 'f data', 'e data', 'f data', 'e data', 'f data', 'e data', 'f data'),
    header=('1st header', '2nd header', '3rd header',
            '4th header', '5th header', '5th header', '5th header', '5th header', '5th header', '5th header',
            '5th header',),
    title='Tables are nonsense', alert=('green', 'some message here'), section=True,
    header_color='red')
print('report_table')
report += r.report_cards(
    ('primary', 'a', 'a'), ('danger', 'a', 'a'),
    section=True, title='title', border_only=True
)
print('report_cards')
report += r.report_footer(message='message', github='a',
                          linkedin='a', email='a', twitter='a', alert=('green', 'some message here'))
r.report_save('test.html', report)
