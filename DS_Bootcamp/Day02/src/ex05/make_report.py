import config
import analytics

if __name__ == '__main__':
    research = analytics.Research(config.file_path)
    values = research.file_reader(config.has_header)
    analytics_class = analytics.Research.Analytics(values)
    orel, reshka = analytics_class.counts()
    frac_orel, frac_reshka = analytics_class.Fractions(orel, reshka)
    counts_of_templates = analytics_class.counts()
    predict_list = analytics_class.predict_random(config.num_of_steps)
    analytics_class_for_predict = analytics.Research.Analytics(predict_list)
    predict_orel, predict_reshka = analytics_class_for_predict.counts()
    analytics_class.save_file(config.template_of_text.format(counts_of_templates, reshka, orel, frac_reshka, frac_orel, config.num_of_steps, predict_reshka, predict_orel), config.file_save_path, config.format_save_file)
    
