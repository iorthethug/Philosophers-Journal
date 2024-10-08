from django.test import TestCase
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APIClient
from .models import Philosopher
from .views import analyze_user_input, match_philosopher, match_philosopher_transformer

# Create your tests here.

class PhilosopherModelTestCase(TestCase):

    def setUp(self):
        self.client = APIClient()

        self.philosopher = Philosopher.objects.create(
            name='Plato',
            bio='Plato was an ancient Greek philosopher who was a student of Socrates and the teacher of Aristotle.',
            school_of_thought='Platonism',
            core_ideas=['Idealism', 'Theory of Forms'],
            tone='Neutral',
            works=['The Republic', 'Symposium'],
            era='Ancient',
            quotes=['"Courage is knowing what not to fear."'],
        )

        self.philosopher = Philosopher.objects.create(
            name='Aristotle',
            bio='Aristotle was an ancient Greek philosopher and scientist who was a student of Plato and the teacher of Alexander the Great.',
            school_of_thought='Aristotelianism',
            core_ideas=['Logic', 'Ethics'],
            tone='Neutral',
            works=['Nicomachean Ethics', 'Politics'],
            era='Ancient',
            quotes=['"We are what we repeatedly do. Excellence, then, is not an act, but a habit."'],
        )

        self.philosopher = Philosopher.objects.create(
            name='Kant',
            bio="Immanuel Kant was a German philosopher and a central figure in modern philosophy. His critical philosophy synthesized rationalism and empiricism, and he is best known for his work on metaphysics, epistemology, and ethics. His 'Critique of Pure Reason' profoundly influenced subsequent philosophical thought. Deontological Ethics (Duty and Morality): Kant's moral philosophy is grounded in the idea of duty rather than consequence. He argued that actions are morally right if they are done out of duty and according to universal principles (the Categorical Imperative).Categorical Imperative: Kant’s most famous idea, which states that you should act only according to the maxim that you would want to become a universal law. This principle emphasizes the universality and necessity of moral actions.Autonomy and Rationality: Kant believed that humans, as rational beings, have the ability to govern themselves through reason. He argued that moral autonomy (self-legislation) is central to human dignity and freedom.Phenomena and Noumena: In his Critique of Pure Reason, Kant made a distinction between phenomena (things as we experience them) and noumena (things as they are in themselves). He argued that we can never fully know the noumenal world, only the world as it appears to us.Moral Law and Free Will: Kant believed in free will, and that moral law comes from reason. He argued that individuals are morally obligated to act in accordance with moral law, not based on desires or inclinations.Perpetual Peace: Kant also had a significant impact on political philosophy. He wrote an essay titled 'Perpetual Peace,' where he outlined conditions for lasting peace, including republican constitutions and the idea of a federation of free states.How did Kant start his day? He got up at 5:00 A.M. His servant Martin Lampe, who worked for him from at least 1762 until 1802, would wake him. The old soldier was under orders to be persistent, so that Kant would not sleep longer. Kant was proud that he never got up even half an hour late, even though he found it hard to get up early. It appears that during his early years, he did sleep in at times. After getting up, Kant would drink one or two cups of tea -- weak tea. With that, he smoked a pipe of tobacco. The time he needed for smoking it 'was devoted to meditation.' Apparently, Kant had formulated the maxim for himself that he would smoke only one pipe, but it is reported that the bowls of his pipes increased considerably in size as the years went on. He then prepared his lectures and worked on his books until 7:00. His lectures began at 7:00, and they would last until 11:00. With the lectures finished, he worked again on his writings until lunch. Go out to lunch, take a walk, and spend the rest of the afternoon with his friend Green. After going home, he would do some more light work and read.",
            school_of_thought='Kantianism',
            core_ideas=['Categorical Imperative', 'Deontology'],
            tone='Neutral',
            works=['Critique of Pure Reason', 'Groundwork of the Metaphysics of Morals'],
            era='Modern',
            quotes=['"Act only according to that maxim whereby you can at the same time will that it should become a universal law."'],
        )
        
        # philosopher with negative tone
        self.philosopher = Philosopher.objects.create(
            name='Nietzsche',
            bio="Friedrich Nietzsche was a German philosopher, cultural critic, and poet. Nihilism: Nietzsche is famous for his exploration of nihilism—the belief that life has no inherent meaning. He believed that with the 'death of God' (the decline of religious belief), traditional values lost their foundation, and individuals are left to create their own meaning. Will to Power: This is one of Nietzsche's most central ideas. He believed that the fundamental driving force in humans is not survival or pleasure, but a deep desire for power and mastery over oneself and the world. Übermensch (Superman): Nietzsche introduced the concept of the Übermensch, or 'Overman,' a figure who transcends conventional morality to create his own values and live authentically. Eternal Recurrence: A thought experiment where Nietzsche asks us to imagine living the same life over and over again. He argues that only those who embrace life fully, without regret, can accept this concept. Master-Slave Morality: Nietzsche contrasts 'master morality,' which values strength, creativity, and power, with 'slave morality,' which values humility, meekness, and pity, originating from the oppressed. Critique of Christianity and Morality: Nietzsche was highly critical of Christianity, believing it promotes weakness and mediocrity through its moral code of compassion and humility.",
            school_of_thought='Nihilism',
            core_ideas=['Will to Power', 'Eternal Recurrence'],
            tone='Negative',
            works=['Thus Spoke Zarathustra', 'Beyond Good and Evil'],
            era='Modern',
            quotes=['God is dead.'],
        )
        
        # philosopher with positive tone
        self.philosopher = Philosopher.objects.create(
            name='Confucius',
            bio='Confucius was a Chinese philosopher and politician who is known for his teachings on ethics and morality.',
            school_of_thought='Confucianism',
            core_ideas=['Ren', 'Li'],
            tone='Positive',
            works=['Analects', 'The Great Learning'],
            era='Ancient',
            quotes=['"It does not matter how slowly you go as long as you do not stop."'],
        )
   
    def test_philosopher_exists(self):
        philosopher = Philosopher.objects.all()
        #check that its 5 philosophers
        self.assertEqual(philosopher.count(), 5)
    '''
    def test_analyze_user_input_neutral(self):
        user_text = 'What is the meaning of life?'
        keywords, sentiment, embeddings = analyze_user_input(user_text)
        self.assertEqual(keywords, ['what', 'is', 'the', 'meaning', 'of', 'life', '?'])
        self.assertEqual(sentiment, 'Neutral')
    
    def test_philosopher_matching(self):
        user_text = 'What is the meaning of life?'
        matched_philosopher = match_philosopher(user_text)
        self.assertEqual(matched_philosopher, Philosopher.objects.get(name='Plato'))
    '''
    '''
    def test_philosopher_transformer_matching(self):
        user_text = 'What is the meaning of life?. Im just think neutrally about it.'
        matched_philosopher = match_philosopher_transformer(user_text)
        self.assertEqual(matched_philosopher, Philosopher.objects.get(name='Kant'))
    '''
    def test_philosopher_transformer_matching_negative(self):
        user_text = 'Woke up today feeling drained, even though I got a full night of sleep. I don’t get it—why do I always feel like I need more rest? It’s frustrating. I’ve got that meeting at 10, and honestly, I’m not looking forward to it. Just the thought of it makes me feel tired already. I hope it doesn’t drag on forever. I don’t have the energy for long meetings today. I’ve been telling myself I’ll go to the gym, but I’ve been avoiding it all week. Maybe it’s the lack of motivation, or maybe I’m just too tired to even think about it.I don’t know why, but lately, everything feels a bit… off. Like I’m just going through the motions. I’m not exactly excited about anything either.'
        matched_philosopher = match_philosopher_transformer(user_text)
        self.assertEqual(matched_philosopher, Philosopher.objects.get(name='Nietzsche'))
    '''
    def test_philosopher_transformer_matching_positive(self):
        user_text = 'Woke up feeling surprisingly good today. For once, I don’t feel completely exhausted, which is nice. The sun’s out, and it’s already brightening my mood. I’ve got that meeting at 10, but I’m not too worried about it. If I stay on top of things, it should go smoothly, and then I can knock out some other tasks. Maybe today will actually be productive. I’ve been telling myself to get back to the gym, and honestly, I think today might be the day. I just have a feeling I’ll have the energy to do it. I always feel so much better when I get some exercise in, and I could definitely use the boost. It’s time to break the slump I’ve been in lately. I’ve also been trying to remind myself that things are moving in the right direction, even when it doesn’t always feel like it. Progress might be slow, but it’s there. I just need to keep pushing forward and stay focused on the bigger picture. I think tonight, after I’ve crossed off my to-do list, I’ll finally start that new show.'
        matched_philosopher = match_philosopher_transformer(user_text)
        self.assertEqual(matched_philosopher, Philosopher.objects.get(name='Confucius'))
    '''
    '''
    def test_user_input_view(self):
        response = self.client.post(reverse('user_input'), {'user_text': 'What is the meaning of life?'})
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertContains(response, 'Plato')

    def test_analyze_user_input_negative(self):
        user_text = 'I hate everything.'
        keywords, sentiment, embeddings = analyze_user_input(user_text)
        self.assertEqual(keywords, ['i', 'hate', 'everything', '.'])
        self.assertEqual(sentiment, 'Negative')

    def test_analyze_user_input_positive(self):
        user_text = 'I love everything.'
        keywords, sentiment, embeddings = analyze_user_input(user_text)
        self.assertEqual(keywords, ['i', 'love', 'everything', '.'])
        self.assertEqual(sentiment, 'Positive')
    '''