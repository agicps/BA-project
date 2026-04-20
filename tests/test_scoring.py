import sys
import unittest
from pathlib import Path
from unittest.mock import patch


PROJECT_ROOT = Path(__file__).resolve().parents[1]
SRC_DIR = PROJECT_ROOT / "src"
if str(SRC_DIR) not in sys.path:
    sys.path.insert(0, str(SRC_DIR))

from scoring import (
    facitRelevantChange,
    facitScoreCalculator,
    uebelkeitScoreCalculator,
    pgsgaScoreCalculator,
    omdqScoreCalculator,
    mainScoreCalculator,
)


class ScoringTests(unittest.TestCase):
    def test_facit_score_calculator_uses_all_answer_types(self):
        session = {
            "id_patient": "patient-1",
            "questionnaire_title": "FACIT-Erschöpfung",
            "date": "2026-04-01",
            "answers": [
                {"question_title": "Ich bin erschöpft.", "value": "0"},
                {"question_title": "Ich fühle mich insgesamt schwach.", "value": "0"},
                {"question_title": "Ich fühle mich lustlos (ausgelaugt).", "value": "0"},
                {"question_title": "Ich bin müde.", "value": "0"},
                {"question_title": "Es fällt mir schwer, etwas anzufangen, weil ich müde bin.", "value": "0"},
                {"question_title": "Es fällt mir schwer, etwas zu Ende zu führen, weil ich müde bin.", "value": "0"},
                {"question_title": "Ich habe das Bedürfnis, tagsüber zu schlafen.", "value": "0"},
                {"question_title": "Ich bin zu müde, um zu essen.", "value": "0"},
                {"question_title": "Ich brauche Hilfe bei meinen gewohnten Aktivitäten (Beruf, Einkaufen, Schule, Freizeit, Sport usw.).", "value": "0"},
                {"question_title": "Ich bin frustriert, weil ich zu müde bin, die Dinge zu tun, die ich machen möchte.", "value": "0"},
                {"question_title": "Ich musste meine sozialen Aktivitäten einschränken, weil ich müde bin.", "value": "0"},
                {"question_title": "Ich habe Energie.", "value": "4"},
                {"question_title": "Ich bin in der Lage meinen gewohnten Aktivitäten nachzugehen (Beruf, Einkaufen, Schule, Freizeit, Sport usw.).", "value": "4"},
            ],
        }

        result = facitScoreCalculator(session)

        self.assertEqual(
            result,
            {
                "id_patient": "patient-1",
                "questionnaire_title": "FACIT-Erschöpfung",
                "date": "2026-04-01",
                "score": 52,
            },
        )

    def test_facit_score_calculator_ignores_duplicate_question_rows(self):
        session = {
            "id_patient": "patient-1",
            "questionnaire_title": "FACIT-Erschöpfung",
            "date": "2026-04-01",
            "answers": [
                {"question_title": "Ich bin erschöpft.", "value": "0"},
                {"question_title": "Ich bin erschöpft.", "value": "0"},
                {"question_title": "Ich fühle mich insgesamt schwach.", "value": "0"},
                {"question_title": "Ich fühle mich insgesamt schwach.", "value": "0"},
                {"question_title": "Ich fühle mich lustlos (ausgelaugt).", "value": "0"},
                {"question_title": "Ich fühle mich lustlos (ausgelaugt).", "value": "0"},
                {"question_title": "Ich bin müde.", "value": "0"},
                {"question_title": "Ich bin müde.", "value": "0"},
                {"question_title": "Es fällt mir schwer, etwas anzufangen, weil ich müde bin.", "value": "0"},
                {"question_title": "Es fällt mir schwer, etwas anzufangen, weil ich müde bin.", "value": "0"},
                {"question_title": "Es fällt mir schwer, etwas zu Ende zu führen, weil ich müde bin.", "value": "0"},
                {"question_title": "Es fällt mir schwer, etwas zu Ende zu führen, weil ich müde bin.", "value": "0"},
                {"question_title": "Ich habe das Bedürfnis, tagsüber zu schlafen.", "value": "0"},
                {"question_title": "Ich habe das Bedürfnis, tagsüber zu schlafen.", "value": "0"},
                {"question_title": "Ich bin zu müde, um zu essen.", "value": "0"},
                {"question_title": "Ich bin zu müde, um zu essen.", "value": "0"},
                {"question_title": "Ich brauche Hilfe bei meinen gewohnten Aktivitäten (Beruf, Einkaufen, Schule, Freizeit, Sport usw.).", "value": "0"},
                {"question_title": "Ich brauche Hilfe bei meinen gewohnten Aktivitäten (Beruf, Einkaufen, Schule, Freizeit, Sport usw.).", "value": "0"},
                {"question_title": "Ich bin frustriert, weil ich zu müde bin, die Dinge zu tun, die ich machen möchte.", "value": "0"},
                {"question_title": "Ich bin frustriert, weil ich zu müde bin, die Dinge zu tun, die ich machen möchte.", "value": "0"},
                {"question_title": "Ich musste meine sozialen Aktivitäten einschränken, weil ich müde bin.", "value": "0"},
                {"question_title": "Ich musste meine sozialen Aktivitäten einschränken, weil ich müde bin.", "value": "0"},
                {"question_title": "Ich habe Energie.", "value": "4"},
                {"question_title": "Ich habe Energie.", "value": "4"},
                {"question_title": "Ich bin in der Lage meinen gewohnten Aktivitäten nachzugehen (Beruf, Einkaufen, Schule, Freizeit, Sport usw.).", "value": "4"},
                {"question_title": "Ich bin in der Lage meinen gewohnten Aktivitäten nachzugehen (Beruf, Einkaufen, Schule, Freizeit, Sport usw.).", "value": "4"},
            ],
        }

        result = facitScoreCalculator(session)

        self.assertEqual(result["score"], 52)

    def test_uebelkeit_score_calculator(self):
        session = {
            "id_patient": "patient-1",
            "questionnaire_title": "Übelkeit/Erbrechen",
            "date": "2026-04-01",
            "answers": [
                {"question_title": "Häufigkeit: Wie häufig müssen Sie am Tag erbrechen?", "value": "12XProTag"},
            ],
        }

        result = uebelkeitScoreCalculator(session)

        self.assertEqual(
            result,
            {
                "id_patient": "patient-1",
                "questionnaire_title": "Übelkeit/Erbrechen",
                "date": "2026-04-01",
                "score": 1,
            },
        )

    def test_pgsga_score_calculator(self):
        session = {
            "id_patient": "patient-1",
            "questionnaire_title": "PG-SGA SF | Patientenbezogenes Ernährungsassesment",
            "date": "2026-04-01",
            "answers": [
                {"question_title": "In den vergangenen zwei Wochen hat sich mein Gewicht:", "value": "2"},
                {"question_title": "Im Vergleich zu meiner normalen Nahrungsaufnahme würde ich diese im vergangenen Monat wie folgt bewerten:", "value": "1"},
                {"question_title": "Derzeit nehme ich folgende Nahrung auf:", "value": "0"},
                {"question_title": "Mein Aktivitätsniveau in den letzten vier  Wochen würde ich allgemein wie folgt bewerten:", "value": "1"},
            ],
        }

        result = pgsgaScoreCalculator(session)

        self.assertEqual(result["id_patient"], "patient-1")
        self.assertEqual(result["questionnaire_title"], "PG-SGA SF | Patientenbezogenes Ernährungsassesment")
        self.assertEqual(result["date"], "2026-04-01")
        self.assertEqual(result["score"], 4)

    def test_omdq_score_calculator(self):
        session = {
            "id_patient": "patient-1",
            "questionnaire_title": "OMDQ",
            "date": "2026-04-01",
            "answers": [
                {"question_title": "1. Wie würden Sie Ihre allgemeine Befindlichkeit in den letzten 24 Stunden einschätzen?", "value": "2"},
                {"question_title": "2. Wie stark waren Ihre Mund- und Rachenschmerzen in den letzten 24 Stunden?", "value": "keineSchmerzen"},
                {"question_title": "3. Wie stark schränkte Sie der Mund- und Rachenschmerz in den letzten 24 Stunden bei den folgenden Tätigkeiten ein?", "value": "keineEinschrankung"},
                {"question_title": "4. Wie stark hatten Sie in den letzten 24 Stunden Durchfall?", "value": "keinDurchfall"},
            ],
        }

        result = omdqScoreCalculator(session)

        self.assertEqual(result["id_patient"], "patient-1")
        self.assertEqual(result["questionnaire_title"], "OMDQ")
        self.assertEqual(result["date"], "2026-04-01")
        self.assertAlmostEqual(result["score"], 0.5)

    def test_main_score_calculator_groups_sessions_by_patient(self):
        sessions = [
            {
                "id_patient": "patient-1",
                "questionnaire_title": "FACIT-Erschöpfung",
                "date": "2026-04-01",
                "answers": [
                    {"question_title": "Ich bin erschöpft.", "value": "0"},
                    {"question_title": "Ich habe Energie.", "value": "4"},
                    {"question_title": "Ich bin in der Lage meinen gewohnten Aktivitäten nachzugehen (Beruf, Einkaufen, Schule, Freizeit, Sport usw.).", "value": "4"},
                ],
            },
            {
                "id_patient": "patient-1",
                "questionnaire_title": "FACIT-Erschöpfung",
                "date": "2026-04-03",
                "answers": [
                    {"question_title": "Ich bin erschöpft.", "value": "1"},
                    {"question_title": "Ich habe Energie.", "value": "3"},
                    {"question_title": "Ich bin in der Lage meinen gewohnten Aktivitäten nachzugehen (Beruf, Einkaufen, Schule, Freizeit, Sport usw.).", "value": "4"},
                ],
            },
            {
                "id_patient": "patient-2",
                "questionnaire_title": "OMDQ",
                "date": "2026-04-02",
                "answers": [
                    {"question_title": "1. Wie würden Sie Ihre allgemeine Befindlichkeit in den letzten 24 Stunden einschätzen?", "value": "1"},
                    {"question_title": "2. Wie stark waren Ihre Mund- und Rachenschmerzen in den letzten 24 Stunden?", "value": "keineSchmerzen"},
                    {"question_title": "3. Wie stark schränkte Sie der Mund- und Rachenschmerz in den letzten 24 Stunden bei den folgenden Tätigkeiten ein?", "value": "keineEinschrankung"},
                    {"question_title": "4. Wie stark hatten Sie in den letzten 24 Stunden Durchfall?", "value": "keinDurchfall"},
                ],
            },
        ]

        result = mainScoreCalculator(sessions)

        patient_1_scores = result["patient-1"]
        facit_scores = patient_1_scores["FACIT-Erschöpfung"]
        patient_2_scores = result["patient-2"]

        self.assertEqual(len(facit_scores), 2)
        self.assertEqual(
            [entry["date"] for entry in facit_scores],
            ["2026-04-01", "2026-04-03"],
        )
        self.assertAlmostEqual(patient_2_scores["OMDQ"][0]["score"], 0.25)

    def test_main_score_calculator_raises_on_unknown_questionnaire(self):
        sessions = [
            {
                "id_patient": "patient-1",
                "questionnaire_title": "Unknown questionnaire",
                "date": "2026-04-01",
                "answers": [],
            }
        ]

        with self.assertRaisesRegex(ValueError, "Nicht unterstützter Fragebogentitel: Unknown questionnaire"):
            mainScoreCalculator(sessions)

    def test_main_score_calculator_raises_when_calculator_returns_none(self):
        sessions = [
            {
                "id_patient": "patient-1",
                "questionnaire_title": "FACIT-Erschöpfung",
                "date": "2026-04-01",
                "answers": [],
            }
        ]

        with patch('scoring.facitScoreCalculator', return_value=None):
            with self.assertRaisesRegex(ValueError, "Score-Kalkulator für Fragebogen 'FACIT-Erschöpfung' hat None für Patient patient-1 zurückgegeben"):
                mainScoreCalculator(sessions)

    def test_facit_relevant_change_sorts_dates_before_comparing(self):
        facit_scores = [
            {"date": "2026-04-03", "score": 18},
            {"date": "2026-04-01", "score": 10},
        ]

        self.assertEqual(
            facitRelevantChange(facit_scores),
            "Clinically meaningful improvement",
        )


if __name__ == "__main__":
    unittest.main()