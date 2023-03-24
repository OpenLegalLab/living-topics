from transformers import pipeline

fill_mask = pipeline(model="ZurichNLP/swissbert")

fill_mask.model.set_default_language("de_CH")

fill_mask("Sanierung von asbestbelasteten Gebäude ist Sache der <mask>.")
