import pandas as pd
from scipy import stats
from statsmodels.stats.anova import anova_lm
from statsmodels.formula.api import ols
from statsmodels.stats.multicomp import pairwise_tukeyhsd
from statsmodels.graphics.mosaicplot import mosaic
import matplotlib.pyplot as plt
import dataframe_image as dfi

# Loading the survey data into a dataframe
data = pd.read_excel("data/survey_data.xlsx", header=0)

COLOR = "orange"
FONTSIZE_TITLE = 10
SAVE = True

def test_question_a():
    # QUESTION A: In general, is one system preferred over the other?
    preferences = data["Which chatbot do you prefer?"]
    counts = preferences.groupby(preferences).count()
    p_value = stats.binomtest(counts["System A"] + int(0.5*counts["No preference"]),
                            n = counts.sum(),
                            p = 0.5,
                            alternative = "less")

    ax = counts.plot(kind="bar",
                     grid=True,
                     color=COLOR)
    ax.set_xticklabels(counts.index, rotation=0)
    ax.set_ylim(0, 25)
    ax.set_ylabel("Number of participants").set_fontweight("bold")
    ax.set_xlabel("Chatbot preference").set_fontweight("bold")
    ax.set_title("Frequency of user preferences", fontsize=FONTSIZE_TITLE, fontweight="bold")
    if SAVE:
        plt.savefig(f"system_preference.png")
    plt.show()

    return p_value


def test_question_b():
    # QUESTION B: Is preferred communication style independent of age?
    # https://www.statstest.com/fischers-exact-test/
    table_data = pd.crosstab(data["Which chatbot do you prefer?"], data["What is your age?"]).drop("No preference")
    table_data["18 - 30"] = table_data["18 - 20"] + table_data["20 - 30"]
    table_data["> 40"] = table_data["40 - 50"] + table_data["50 - 60"] + table_data["60 - 70"]
    table_data = table_data[["18 - 30", "> 40"]]
    odds_ratio, p_value = stats.fisher_exact(table_data.values)

    mosaic_data = data[["Which chatbot do you prefer?", "What is your age?"]]
    mosaic_data = mosaic_data.drop(mosaic_data[mosaic_data["Which chatbot do you prefer?"] == "No preference"].index)
    mosaic_data.loc[(mosaic_data["What is your age?"] == "18 - 20") |
                    (mosaic_data["What is your age?"] == "20 - 30"), "What is your age?"] = "18 - 30"
    mosaic_data.loc[(mosaic_data["What is your age?"] == "40 - 50") |
                    (mosaic_data["What is your age?"] == "50 - 60") |
                    (mosaic_data["What is your age?"] == "60 - 70"), "What is your age?"] = "> 40"

    def get_color(key):
        keys = [('18 - 30', 'System B'), ('18 - 30', 'System A'), ('> 40', 'System B'), ('> 40', 'System A')]
        colors = ["darkorange", "orange", "navajowhite", "blanchedalmond"]
        return colors[keys.index(key)]

    fig, rects =mosaic(mosaic_data,
           ["What is your age?", "Which chatbot do you prefer?"],
           properties=lambda key: {'color': get_color(key)})
    fig.suptitle("Mosaic plot of system preference and age group", fontsize=FONTSIZE_TITLE, fontweight="bold")
    if SAVE:
        plt.savefig("mosaic.png")
    plt.show()
    return odds_ratio, p_value


def test_question_c(system_variant):
    # QUESTION C: Do perceived English difficulty and familiarity with chatbots have an effect on user satisfaction?

    # Collecting and preparing the data for the test
    table_data= data[[f"How satisfied are you with the experience of system {system_variant}",
                      "How was the English level of the chatbots for you? [Difficulty]",
                      "How often do you use chatbots? [Frequency]"]]

    table_data = table_data.rename(columns={f"How satisfied are you with the experience of system {system_variant}": "satisfaction",
                                            "How was the English level of the chatbots for you? [Difficulty]": "english",
                                            "How often do you use chatbots? [Frequency]": "experience"})

    # Conducting the test
    model = ols("satisfaction ~ C(english) + C(experience) + C(english):C(experience)", data=table_data).fit()
    anova_output = anova_lm(model, type=2).rename(columns={'PR(>F)': 'p-value'})

    # If the output of the ANOVA indicates an effect of english or experience on satisfaction,
    # a post-hoc test can be conducted. However, in our case it turns out this is not necessary. We therefore do not
    # necessarily need the output of the following two lines of code.
    tukey_results_english = pairwise_tukeyhsd(table_data['satisfaction'], table_data['english'], alpha=0.05)
    tukey_results_experience = pairwise_tukeyhsd(table_data['satisfaction'], table_data['experience'], alpha=0.05)

    data_english = table_data[["satisfaction"]].groupby(table_data["english"]).mean().reindex(["Very easy", "Easy", "Neutral", "Difficult"])
    data_experience = table_data[["satisfaction"]].groupby(table_data["experience"]).mean().reindex(["Never", "Seldom", "Sometimes", "Often", "Almost always"])

    ax = data_english.plot(kind="bar",
                           grid=True,
                           color=COLOR)
    ax.set_xticklabels(data_english.index, rotation=0)
    ax.set_ylim(0, 10)
    ax.get_legend().remove()
    ax.set_ylabel("Average satisfaction score").set_fontweight("bold")
    ax.set_xlabel("Perceived English difficulty").set_fontweight("bold")
    ax.set_title(f"Average satisfaction score\n vs.\n perceived English difficulty (system {system_variant})", fontsize=FONTSIZE_TITLE, fontweight="bold")
    if SAVE:
        plt.savefig(f"satisfaction_english_{system_variant}.png")
        dfi.export(anova_output.round(3), "satisfaction_anova.png")
    plt.show()

    ax = data_experience.plot(kind="bar",
                              grid=True,
                              color=COLOR)
    ax.set_xticklabels(data_experience.index, rotation=0)
    ax.set_ylim(0, 10)
    ax.get_legend().remove()
    ax.set_ylabel("Average satisfaction score").set_fontweight("bold")
    ax.set_xlabel("Chatbot use frequency").set_fontweight("bold")
    ax.set_title(f"Average satisfaction score\n vs.\n chatbot use frequency (system {system_variant})", fontsize=FONTSIZE_TITLE,
                 fontweight="bold")
    if SAVE:
        plt.savefig(f"satisfaction_usefrequency_{system_variant}.png")
    plt.show()

    return anova_output, tukey_results_english, tukey_results_experience


def test_question_d(system_variant):
    # QUESTION D: Do perceived English difficulty and familiarity with chatbots have an
    # effect on users willingness to recommend the system to others?

    # Collecting and preparing the data for the test
    table_data = data[[f"How likely are you to recommend system {system_variant} to your family/friends?",
                       "How was the English level of the chatbots for you? [Difficulty]",
                       "How often do you use chatbots? [Frequency]"]]

    table_data = table_data.\
            rename(columns={f"How likely are you to recommend system {system_variant} to your family/friends?": "recommend",
                                "How was the English level of the chatbots for you? [Difficulty]": "english",
                                "How often do you use chatbots? [Frequency]": "experience"})

    # Conducting the test
    model = ols("recommend ~ C(english) + C(experience) + C(english):C(experience)", data=table_data).fit()
    anova_output = anova_lm(model, type=2).rename(columns={'PR(>F)': 'p-value'})

    # If the output of the ANOVA indicates an effect of english or experience on satisfaction,
    # a post-hoc test can be conducted. However, in our case it turns out this is not necessary. We therefore do not
    # necessarily need the output of the following two lines of code.
    tukey_results_english = pairwise_tukeyhsd(table_data['recommend'], table_data['english'], alpha=0.05)
    tukey_results_experience = pairwise_tukeyhsd(table_data['recommend'], table_data['experience'], alpha=0.05)

    data_english = table_data[["recommend"]].groupby(table_data["english"]).mean().reindex(["Very easy", "Easy", "Neutral", "Difficult"])
    data_experience = table_data[["recommend"]].groupby(table_data["experience"]).mean().reindex(["Never", "Seldom", "Sometimes", "Often", "Almost always"])

    ax = data_english.plot(kind="bar",
                     color = COLOR,
                     grid=True)
    ax.set_xticklabels(data_english.index, rotation=0)
    ax.set_ylim(0, 10)
    ax.get_legend().remove()
    ax.set_ylabel("Average recommendation likelihood score").set_fontweight("bold")
    ax.set_xlabel("Perceived English difficulty").set_fontweight("bold")
    ax.set_title(f"Average recommendation likelihood score\n vs.\n perceived English difficulty (system {system_variant})", fontsize=FONTSIZE_TITLE,
                 fontweight="bold")
    if SAVE:
        plt.savefig(f"recommend_english_{system_variant}.png")
        dfi.export(anova_output.round(3), "recommendation_anova.png")
    plt.show()

    ax = data_experience.plot(kind="bar",
                              color = COLOR,
                              grid=True)
    ax.set_xticklabels(data_experience.index, rotation=0)
    ax.set_ylim(0, 10)
    ax.get_legend().remove()
    ax.set_ylabel("Average recommendation likelihood score").set_fontweight("bold")
    ax.set_xlabel("Chatbot use frequency").set_fontweight("bold")
    ax.set_title(f"Average recommendation likelihood score\n vs.\n chatbot use frequency (system {system_variant})", fontsize=FONTSIZE_TITLE,
                 fontweight="bold")
    if SAVE:
        plt.savefig(f"recommend_usefrequency_{system_variant}.png")
    plt.show()

    return anova_output, tukey_results_english, tukey_results_experience


def test_all():
    # Question a
    binomial_test_p_value = test_question_a()

    # Question b
    fisher_exact_odds_ratio, fisher_exact_p_value = test_question_b()

    # Question c
    ANOVA_result_question_c_sysA, _, _ = test_question_c("A")
    ANOVA_result_question_c_sysB, _, _ = test_question_c("B")

    # Question d
    ANOVA_result_question_d_sysA, _, _ = test_question_d("A")
    ANOVA_result_question_d_sysB, _, _ = test_question_d("B")

    print(f"Q.A: Binomial test results: {binomial_test_p_value}\n")
    print(f"Q.B: P-value Fisher's exact test: {fisher_exact_p_value}\n")
    print("Q.C(1): Result ANOVA: Satisfaction ~ english + experience + english:experience (system A)\n")
    print(ANOVA_result_question_c_sysA, "\n\n")
    print("Q.C(2): Result ANOVA: Satisfaction ~ english + experience + english:experience (system B)\n")
    print(ANOVA_result_question_c_sysB, "\n\n")
    print("Q.D(1): Result ANOVA: Recommendation likeliness ~ english + experience + english:experience (system A)\n")
    print(ANOVA_result_question_d_sysA, "\n\n")
    print("Q.D(2): Result ANOVA: Recommendation likeliness ~ english + experience + english:experience (system B)\n")
    print(ANOVA_result_question_d_sysB)

test_all()