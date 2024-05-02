import unittest
import gcode


class GCode_Test(unittest.TestCase):
    def test_can_parse_file_without_breaking(self):
        parser = gcode.GCodeParser()
        with open('boomerangv4.ncc') as f:
            for line in f:
                g = parser.parse(line)
                if g.shouldProcess():
                    self.assertTrue(g.tokens)
                else:
                    self.assertTrue(g.comment)
    
    def test_normalize(self):
        for token, expected_result in self._normalize_cases:
            r = gcode.normalize(token)
            self.assertEqual(r,expected_result)

    def test_tokenize_param(self):
        for code, tokens in self._tokenize_cases:
            r = gcode.GCodeParser.tokenize(code)
        self.assertEqual(r,tokens)

    def test_tokenize_simple(self):
        r = gcode.GCodeParser.tokenize('M3 S0')
        self.assertEqual(r,('M03','S0'))
        
        r = gcode.GCodeParser.tokenize('M 3S 0')        
        self.assertEqual(r,('M03','S0'))

        r = gcode.GCodeParser.tokenize('m3 s0')        
        self.assertEqual(r,('M03','S0'))

    _tokenize_cases=(
        (
            "G0 X11.4158 Y0.5132",
            ("G00","X11.4158","Y0.5132")),
        (
            "G1 F30.0 Z0.0",
            ("G01","F30.0","Z0.0")),
        (
            "G3 F300.0 X12.9975 Y1.714 I0.4346 J1.0696",
            ("G03","F300.0","X12.9975","Y1.714","I0.4346","J1.0696")),
        (
            "G0 Z1.0",
            ("G00","Z1.0",)),
        (
            "G0 X0.4562 Y1.7439",
            ("G00","X0.4562","Y1.7439")),
        (
            "G1 F30.0 Z0.0",
            ("G01","F30.0","Z0.0")),
        (
            "G3 F300.0X2.018 Y0.538 I1.0998 J-0.1898",
            ("G03","F300.0","X2.018","Y0.538","I1.0998","J-0.1898"))
    )
    _normalize_cases=(
        ('F1','F1'),
        ('F01','F01'),
        ('F1.1','F1.1'),
        ('F01','F01'),
        ('G1','G01'),
        ('G1.1','G1.1'),
        ('G11','G11'),
        ('G110','G110'),
        ('M101','M101'),
    )


