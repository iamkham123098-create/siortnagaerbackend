"""
Seeder command to populate the database with dummy data.
Usage: python manage.py seed_data
"""

from django.core.management.base import BaseCommand
from django.utils import timezone
from datetime import timedelta
from core.models import (
    HomePage, OfficeBearer, Activity, Book, BookCategory,
    Event, EventType, EventPhoto, Announcement, ContactInfo
)


class Command(BaseCommand):
    help = 'Seeds the database with dummy data for testing'

    def add_arguments(self, parser):
        parser.add_argument(
            '--clear',
            action='store_true',
            help='Clear existing data before seeding (soft delete)',
        )

    def handle(self, *args, **options):
        if options['clear']:
            self.stdout.write('Clearing existing data (soft delete)...')
            self.clear_data()

        self.stdout.write('Seeding database...')
        
        self.seed_homepage()
        self.seed_office_bearers()
        self.seed_activities()
        self.seed_books()
        self.seed_events()
        self.seed_announcements()
        self.seed_contact_info()

        self.stdout.write(self.style.SUCCESS('Database seeded successfully!'))

    def clear_data(self):
        """Hard delete all existing data."""
        EventPhoto.objects.all().delete()  # Delete first due to FK constraint
        Event.objects.all().delete()
        Activity.objects.all().delete()
        Book.objects.all().delete()
        Announcement.objects.all().delete()
        OfficeBearer.objects.all().delete()
        HomePage.objects.all().delete()
        ContactInfo.objects.all().delete()

    def seed_homepage(self):
        """Create home page content."""
        HomePage.objects.update_or_create(
            is_active=True,
            defaults={
                'hero_title': 'Welcome to SIO RT Nagar',
                'hero_subtitle': 'Building Tomorrow\'s Leaders Today - Empowering Youth Through Islamic Values',
                'introduction': '''Students Islamic Organisation (SIO) RT Nagar is a dynamic youth movement 
dedicated to nurturing young minds with Islamic values and contemporary knowledge. 
We strive to create responsible citizens who contribute positively to society while 
staying rooted in their faith. Our chapter has been serving the community since 2010, 
organizing various educational, social, and spiritual programs for students across RT Nagar and surrounding areas.''',
                'vision': '''To be a leading Islamic student movement that nurtures intellectually vibrant, 
morally upright, and socially responsible youth who serve as agents of positive change 
in society while maintaining strong Islamic identity and values.''',
                'mission': '''To empower students with comprehensive Islamic knowledge, 
develop their leadership potential, engage them in community service, 
and prepare them to face contemporary challenges while staying true to Islamic principles. 
We aim to create a balanced generation that excels in both worldly pursuits and spiritual growth.''',
                'cta_join_text': 'Join Our Movement',
                'cta_events_text': 'Explore Events',
            }
        )
        self.stdout.write('  ✓ Home page created')

    def seed_office_bearers(self):
        """Create office bearers."""
        bearers = [
            {'name': 'Mohammed Arif Khan', 'position': 'President', 'contact_number': '+91 9876543210', 'email': 'president@siortnagar.org', 'display_order': 1},
            {'name': 'Abdul Rahman', 'position': 'Vice President', 'contact_number': '+91 9876543211', 'email': 'vp@siortnagar.org', 'display_order': 2},
            {'name': 'Faizan Ahmed', 'position': 'General Secretary', 'contact_number': '+91 9876543212', 'email': 'secretary@siortnagar.org', 'display_order': 3},
            {'name': 'Yusuf Patel', 'position': 'Joint Secretary', 'contact_number': '+91 9876543213', 'email': 'jointsecretary@siortnagar.org', 'display_order': 4},
            {'name': 'Ibrahim Shaikh', 'position': 'Treasurer', 'contact_number': '+91 9876543214', 'email': 'treasurer@siortnagar.org', 'display_order': 5},
            {'name': 'Hamza Ali', 'position': 'Education Secretary', 'contact_number': '+91 9876543215', 'email': 'education@siortnagar.org', 'display_order': 6},
            {'name': 'Bilal Ahmed', 'position': 'Media Secretary', 'contact_number': '+91 9876543216', 'email': 'media@siortnagar.org', 'display_order': 7},
            {'name': 'Usman Khan', 'position': 'Social Service Secretary', 'contact_number': '+91 9876543217', 'email': 'social@siortnagar.org', 'display_order': 8},
        ]

        for bearer_data in bearers:
            OfficeBearer.objects.update_or_create(
                name=bearer_data['name'],
                defaults=bearer_data
            )
        self.stdout.write(f'  ✓ {len(bearers)} office bearers created')

    def seed_activities(self):
        """Create 50 activities with mix of past and current dates."""
        today = timezone.now().date()
        activities = [
            # Recent activities (last 30 days)
            {'title': 'Weekly Quran Study Circle', 'description': 'Join our weekly Quran study session where we explore the meanings and teachings of the Holy Quran. Open to all students regardless of their level of Arabic knowledge. Tafseer discussions and reflections included.', 'activity_date': today - timedelta(days=2)},
            {'title': 'Leadership Development Workshop', 'description': 'A comprehensive workshop focusing on developing essential leadership skills including public speaking, team management, decision-making, and conflict resolution. Certificates will be provided to all participants.', 'activity_date': today - timedelta(days=5)},
            {'title': 'Community Clean-up Drive', 'description': 'Be part of our monthly community service initiative! We cleaned up RT Nagar main roads and parks. Refreshments were served to all volunteers.', 'activity_date': today - timedelta(days=8)},
            {'title': 'Islamic Finance Seminar', 'description': 'Learn about halal investment options, Islamic banking principles, and how to manage finances according to Shariah guidelines. Guest speaker from Islamic Finance Institute.', 'activity_date': today - timedelta(days=12)},
            {'title': 'Youth Career Guidance Session', 'description': 'Expert career counselors guided students on career options, higher education paths, competitive exam preparation, and professional development.', 'activity_date': today - timedelta(days=15)},
            {'title': 'Book Reading Session', 'description': 'Discussion on "Towards Understanding Islam" by Maulana Maududi. Participants shared insights and reflections on key chapters.', 'activity_date': today - timedelta(days=18)},
            {'title': 'Sports Day Event', 'description': 'Annual sports day featuring cricket, football, and indoor games. Over 100 youth participated. Winners received medals and certificates.', 'activity_date': today - timedelta(days=22)},
            {'title': 'Public Speaking Training', 'description': 'Training session to help students overcome stage fear and develop effective communication skills. Practice sessions with feedback provided.', 'activity_date': today - timedelta(days=25)},
            {'title': 'Health Awareness Camp', 'description': 'Free health checkup camp in collaboration with local hospitals. Blood pressure, diabetes, and eye checkups were conducted.', 'activity_date': today - timedelta(days=28)},
            {'title': 'Neighborhood Visit Program', 'description': 'Door-to-door community engagement program to connect with families and understand their needs. Distributed educational pamphlets.', 'activity_date': today - timedelta(days=30)},
            
            # 1-2 months ago
            {'title': 'Ramadan Preparation Workshop', 'description': 'Interactive session on preparing spiritually for Ramadan. Discussed goals, routines, and maximizing the blessed month.', 'activity_date': today - timedelta(days=35)},
            {'title': 'Environmental Awareness Campaign', 'description': 'Planted 50 trees in collaboration with Forest Department. Educated youth about environmental responsibility.', 'activity_date': today - timedelta(days=40)},
            {'title': 'Inter-School Quiz Competition', 'description': 'Islamic knowledge quiz competition with 15 schools participating. Cash prizes and books awarded to winners.', 'activity_date': today - timedelta(days=45)},
            {'title': 'Iftar Distribution Drive', 'description': 'Distributed iftar packets to 500 families in underprivileged areas. Volunteers prepared and packed meals.', 'activity_date': today - timedelta(days=50)},
            {'title': 'Taraweeh Night Program', 'description': 'Special Taraweeh prayers followed by late-night Quran sessions. Scholars delivered short reminders.', 'activity_date': today - timedelta(days=55)},
            {'title': 'Eid Gift Distribution', 'description': 'Distributed Eid gifts and new clothes to 100 orphan children. Joy and happiness shared with the community.', 'activity_date': today - timedelta(days=60)},
            {'title': 'Resume Writing Workshop', 'description': 'Professional workshop on creating effective resumes and cover letters. Mock interviews conducted.', 'activity_date': today - timedelta(days=65)},
            {'title': 'Arabic Language Course - Batch 3', 'description': 'Started new batch for beginners in Arabic language. 30 students enrolled for the 3-month program.', 'activity_date': today - timedelta(days=70)},
            {'title': 'Personality Development Session', 'description': 'Expert psychologist conducted session on building confidence and positive mindset. Highly attended event.', 'activity_date': today - timedelta(days=75)},
            {'title': 'Community Iftar Gathering', 'description': 'Large community iftar with 300+ attendees. Local imam delivered inspiring talk on unity.', 'activity_date': today - timedelta(days=80)},
            
            # 3-4 months ago
            {'title': 'Women Empowerment Workshop', 'description': 'Session for mothers and sisters on Islamic rights of women, financial literacy, and self-development.', 'activity_date': today - timedelta(days=90)},
            {'title': 'Youth Hiking Trip', 'description': 'Adventure trip to nearby hills combining nature appreciation with team building. 40 youth participated.', 'activity_date': today - timedelta(days=95)},
            {'title': 'Debate Competition', 'description': 'Inter-college debate on "Role of Youth in Nation Building". Three colleges participated.', 'activity_date': today - timedelta(days=100)},
            {'title': 'First Aid Training', 'description': 'Red Cross conducted first aid and emergency response training. Participants received certificates.', 'activity_date': today - timedelta(days=105)},
            {'title': 'Islamic Art Workshop', 'description': 'Calligraphy and Islamic geometric art workshop. Materials provided. Beautiful artworks created.', 'activity_date': today - timedelta(days=110)},
            {'title': 'Blood Donation Drive', 'description': 'Collected 75 units of blood in collaboration with Blood Bank. All donors received health certificates.', 'activity_date': today - timedelta(days=115)},
            {'title': 'Essay Writing Competition', 'description': 'Essay competition on "Islamic Values in Modern World". Top 3 essays published in newsletter.', 'activity_date': today - timedelta(days=120)},
            {'title': 'Orphanage Visit', 'description': 'Spent quality time with orphan children. Distributed books, toys, and shared meals together.', 'activity_date': today - timedelta(days=125)},
            {'title': 'Film Screening: Message', 'description': 'Screened the movie "The Message" followed by discussion on early Islamic history.', 'activity_date': today - timedelta(days=130)},
            {'title': 'Coding Workshop for Beginners', 'description': 'Introduction to Python programming for school students. Hands-on exercises completed.', 'activity_date': today - timedelta(days=135)},
            
            # 5-6 months ago
            {'title': 'Annual General Meeting 2026', 'description': 'AGM with election of new office bearers. Reports presented and future plans discussed.', 'activity_date': today - timedelta(days=150)},
            {'title': 'New Member Orientation', 'description': 'Orientation program for 25 new members. Explained SIO vision, mission, and activities.', 'activity_date': today - timedelta(days=155)},
            {'title': 'Exam Preparation Workshop', 'description': 'Tips and strategies for board exam preparation. Study materials distributed.', 'activity_date': today - timedelta(days=160)},
            {'title': 'Parent-Teacher Interaction', 'description': 'Meeting with parents to discuss student progress and address concerns.', 'activity_date': today - timedelta(days=165)},
            {'title': 'Documentary Screening', 'description': 'Screening of documentary on Palestine followed by awareness discussion.', 'activity_date': today - timedelta(days=170)},
            {'title': 'Winter Clothes Distribution', 'description': 'Distributed warm clothes to 200 needy families before winter season.', 'activity_date': today - timedelta(days=175)},
            {'title': 'Entrepreneurship Talk', 'description': 'Successful Muslim entrepreneur shared journey and tips for starting business.', 'activity_date': today - timedelta(days=180)},
            {'title': 'Quran Memorization Competition', 'description': 'Competition for memorization of Juz 30. 50 participants from various age groups.', 'activity_date': today - timedelta(days=185)},
            {'title': 'Community Kitchen', 'description': 'Prepared and served meals to 150 homeless people near railway station.', 'activity_date': today - timedelta(days=190)},
            {'title': 'Youth Talent Show', 'description': 'Platform for youth to showcase talents - poetry, nasheed, speeches. Great participation.', 'activity_date': today - timedelta(days=195)},
            
            # 7-12 months ago
            {'title': 'Eid Milad Un Nabi Celebration', 'description': 'Special program on life and teachings of Prophet Muhammad (PBUH). Nasheed performances.', 'activity_date': today - timedelta(days=210)},
            {'title': 'Career Counseling Fair', 'description': 'Representatives from 10 universities provided guidance on higher education options.', 'activity_date': today - timedelta(days=230)},
            {'title': 'Senior Citizens Meet', 'description': 'Spent time with elderly community members. Heard their stories and served refreshments.', 'activity_date': today - timedelta(days=250)},
            {'title': 'Photography Workshop', 'description': 'Professional photographer taught basics of mobile photography. Field trip included.', 'activity_date': today - timedelta(days=270)},
            {'title': 'Independence Day Program', 'description': 'Flag hoisting followed by patriotic speeches and cultural program.', 'activity_date': today - timedelta(days=290)},
            {'title': 'Monsoon Relief Work', 'description': 'Distributed relief materials to flood-affected families in nearby areas.', 'activity_date': today - timedelta(days=310)},
            {'title': 'Science Exhibition', 'description': 'Students displayed science projects. Best projects awarded certificates.', 'activity_date': today - timedelta(days=330)},
            {'title': 'Eid ul Adha Celebration', 'description': 'Community Eid prayers followed by qurbani distribution to needy families.', 'activity_date': today - timedelta(days=350)},
            {'title': 'Summer Camp 2025', 'description': 'Week-long summer camp with educational and recreational activities for children.', 'activity_date': today - timedelta(days=365)},
            {'title': 'Annual Day Celebration 2025', 'description': 'Grand celebration of SIO RT Nagar foundation day with cultural programs.', 'activity_date': today - timedelta(days=380)},
        ]

        for activity_data in activities:
            Activity.objects.update_or_create(
                title=activity_data['title'],
                defaults=activity_data
            )
        self.stdout.write(f'  ✓ {len(activities)} activities created')

    def seed_books(self):
        """Create 50 books for digital library."""
        books = [
            # SIO Literature (25 books)
            {'title': 'Towards Understanding Islam', 'author': 'Syed Abul Ala Maududi', 'category': BookCategory.SIO_LITERATURE, 'drive_link': 'https://drive.google.com/file/d/book1', 'description': 'A comprehensive introduction to the fundamental teachings of Islam covering faith, worship, morality, and social system.'},
            {'title': 'In The Shade of Quran', 'author': 'Syed Qutb', 'category': BookCategory.SIO_LITERATURE, 'drive_link': 'https://drive.google.com/file/d/book2', 'description': 'A thematic commentary on the Quran that explores its spiritual, social, and political dimensions.'},
            {'title': 'The Islamic Movement: Dynamics of Values', 'author': 'Syed Abul Hasan Ali Nadwi', 'category': BookCategory.SIO_LITERATURE, 'drive_link': 'https://drive.google.com/file/d/book3', 'description': 'Analysis of Islamic movements and their role in social transformation.'},
            {'title': 'Student Life and Discipline', 'author': 'SIO India', 'category': BookCategory.SIO_LITERATURE, 'drive_link': 'https://drive.google.com/file/d/book4', 'description': 'A guide for students on managing academic life, time management, and character building.'},
            {'title': 'Milestones', 'author': 'Syed Qutb', 'category': BookCategory.SIO_LITERATURE, 'drive_link': 'https://drive.google.com/file/d/book5', 'description': 'A manifesto for Islamic revival and social change. One of the most influential Islamic texts.'},
            {'title': 'Fundamentals of Islam', 'author': 'Syed Abul Ala Maududi', 'category': BookCategory.SIO_LITERATURE, 'drive_link': 'https://drive.google.com/file/d/book6', 'description': 'Core principles of Islamic faith explained in simple language for modern readers.'},
            {'title': 'Let Us Be Muslims', 'author': 'Syed Abul Ala Maududi', 'category': BookCategory.SIO_LITERATURE, 'drive_link': 'https://drive.google.com/file/d/book7', 'description': 'A call to Muslims to practice their faith with understanding and conviction.'},
            {'title': 'Islamic Way of Life', 'author': 'Syed Abul Ala Maududi', 'category': BookCategory.SIO_LITERATURE, 'drive_link': 'https://drive.google.com/file/d/book8', 'description': 'Comprehensive guide on living according to Islamic principles in daily life.'},
            {'title': 'Witnesses Unto Mankind', 'author': 'Khurram Murad', 'category': BookCategory.SIO_LITERATURE, 'drive_link': 'https://drive.google.com/file/d/book9', 'description': 'The purpose and method of Islamic movement explained with clarity.'},
            {'title': 'In the Early Hours', 'author': 'Khurram Murad', 'category': BookCategory.SIO_LITERATURE, 'drive_link': 'https://drive.google.com/file/d/book10', 'description': 'Reflections on spiritual and self-development from an Islamic perspective.'},
            {'title': 'Way to the Quran', 'author': 'Khurram Murad', 'category': BookCategory.SIO_LITERATURE, 'drive_link': 'https://drive.google.com/file/d/book11', 'description': 'A practical guide on how to approach and benefit from Quran reading.'},
            {'title': 'Islamic Movement - Priorities', 'author': 'Yusuf Al-Qaradawi', 'category': BookCategory.SIO_LITERATURE, 'drive_link': 'https://drive.google.com/file/d/book12', 'description': 'Setting priorities for Islamic workers in contemporary times.'},
            {'title': 'Revival of Religious Sciences', 'author': 'Imam Al-Ghazali', 'category': BookCategory.SIO_LITERATURE, 'drive_link': 'https://drive.google.com/file/d/book13', 'description': 'Classic work on Islamic spirituality, ethics, and worship.'},
            {'title': 'The Sealed Nectar', 'author': 'Safiur Rahman Mubarakpuri', 'category': BookCategory.SIO_LITERATURE, 'drive_link': 'https://drive.google.com/file/d/book14', 'description': 'Award-winning biography of Prophet Muhammad (PBUH).'},
            {'title': 'Stories of the Prophets', 'author': 'Ibn Kathir', 'category': BookCategory.SIO_LITERATURE, 'drive_link': 'https://drive.google.com/file/d/book15', 'description': 'Stories of all prophets from Adam to Muhammad compiled from authentic sources.'},
            {'title': 'Tafsir Ibn Kathir (Abridged)', 'author': 'Ibn Kathir', 'category': BookCategory.SIO_LITERATURE, 'drive_link': 'https://drive.google.com/file/d/book16', 'description': 'Abridged version of the famous Quran commentary by Ibn Kathir.'},
            {'title': 'Riyadh us Saliheen', 'author': 'Imam An-Nawawi', 'category': BookCategory.SIO_LITERATURE, 'drive_link': 'https://drive.google.com/file/d/book17', 'description': 'Collection of authentic hadith on various aspects of Muslim life.'},
            {'title': 'Fortress of the Muslim', 'author': 'Said bin Wahf Al-Qahtani', 'category': BookCategory.SIO_LITERATURE, 'drive_link': 'https://drive.google.com/file/d/book18', 'description': 'Collection of duas and supplications for daily life.'},
            {'title': 'Dont Be Sad', 'author': 'Aaidh ibn Abdullah al-Qarni', 'category': BookCategory.SIO_LITERATURE, 'drive_link': 'https://drive.google.com/file/d/book19', 'description': 'Islamic guide to overcoming depression and finding happiness.'},
            {'title': 'What Islam Is All About', 'author': 'Yahiya Emerick', 'category': BookCategory.SIO_LITERATURE, 'drive_link': 'https://drive.google.com/file/d/book20', 'description': 'Comprehensive textbook on Islam for students and new Muslims.'},
            {'title': 'The Ideal Muslim', 'author': 'Muhammad Ali Al-Hashimi', 'category': BookCategory.SIO_LITERATURE, 'drive_link': 'https://drive.google.com/file/d/book21', 'description': 'Character traits and behavior of an ideal Muslim based on Quran and Sunnah.'},
            {'title': 'The Ideal Muslimah', 'author': 'Muhammad Ali Al-Hashimi', 'category': BookCategory.SIO_LITERATURE, 'drive_link': 'https://drive.google.com/file/d/book22', 'description': 'Guide for Muslim women on personality development and Islamic values.'},
            {'title': 'Noble Life of the Prophet', 'author': 'Ali Muhammad As-Sallaabee', 'category': BookCategory.SIO_LITERATURE, 'drive_link': 'https://drive.google.com/file/d/book23', 'description': 'Detailed biography of Prophet Muhammad (PBUH) with scholarly analysis.'},
            {'title': 'Men Around the Messenger', 'author': 'Khalid Muhammad Khalid', 'category': BookCategory.SIO_LITERATURE, 'drive_link': 'https://drive.google.com/file/d/book24', 'description': 'Biographies of prominent companions of the Prophet.'},
            {'title': 'Women Around the Messenger', 'author': 'Muhammad Ali Qutb', 'category': BookCategory.SIO_LITERATURE, 'drive_link': 'https://drive.google.com/file/d/book25', 'description': 'Stories of notable women during the Prophets time.'},
            
            # Contemporary Literature (25 books)
            {'title': 'The Road to Mecca', 'author': 'Muhammad Asad', 'category': BookCategory.CONTEMPORARY, 'drive_link': 'https://drive.google.com/file/d/book26', 'description': 'An autobiography and travelogue of a European Jewish convert to Islam.'},
            {'title': 'Lost Islamic History', 'author': 'Firas Alkhateeb', 'category': BookCategory.CONTEMPORARY, 'drive_link': 'https://drive.google.com/file/d/book27', 'description': 'Reclaiming Muslim civilization from the past to understand the present.'},
            {'title': 'No God But God', 'author': 'Reza Aslan', 'category': BookCategory.CONTEMPORARY, 'drive_link': 'https://drive.google.com/file/d/book28', 'description': 'The origins, evolution, and future of Islam - a bestselling modern classic.'},
            {'title': 'Purification of the Heart', 'author': 'Hamza Yusuf', 'category': BookCategory.CONTEMPORARY, 'drive_link': 'https://drive.google.com/file/d/book29', 'description': 'Signs, symptoms, and cures of the spiritual diseases of the heart.'},
            {'title': 'Reclaim Your Heart', 'author': 'Yasmin Mogahed', 'category': BookCategory.CONTEMPORARY, 'drive_link': 'https://drive.google.com/file/d/book30', 'description': 'Personal and spiritual development essays for modern Muslims.'},
            {'title': 'Being Muslim: A Practical Guide', 'author': 'Asad Tarsin', 'category': BookCategory.CONTEMPORARY, 'drive_link': 'https://drive.google.com/file/d/book31', 'description': 'Clear, practical guidance on Islamic practice for contemporary life.'},
            {'title': 'The Vision of Islam', 'author': 'Sachiko Murata', 'category': BookCategory.CONTEMPORARY, 'drive_link': 'https://drive.google.com/file/d/book32', 'description': 'Academic introduction to Islamic worldview and civilization.'},
            {'title': 'Islam and the Future of Tolerance', 'author': 'Sam Harris & Maajid Nawaz', 'category': BookCategory.CONTEMPORARY, 'drive_link': 'https://drive.google.com/file/d/book33', 'description': 'A dialogue on reform and the future of Muslim societies.'},
            {'title': 'The Heart of the Quran', 'author': 'Asim Khan', 'category': BookCategory.CONTEMPORARY, 'drive_link': 'https://drive.google.com/file/d/book34', 'description': 'Commentary on Surah Yasin with contemporary insights.'},
            {'title': 'Revive Your Heart', 'author': 'Nouman Ali Khan', 'category': BookCategory.CONTEMPORARY, 'drive_link': 'https://drive.google.com/file/d/book35', 'description': 'Putting life in perspective through Quran and Sunnah.'},
            {'title': 'Muhammad: His Life Based on Earliest Sources', 'author': 'Martin Lings', 'category': BookCategory.CONTEMPORARY, 'drive_link': 'https://drive.google.com/file/d/book36', 'description': 'Beautifully written biography of the Prophet using classical sources.'},
            {'title': 'In the Footsteps of the Prophet', 'author': 'Tariq Ramadan', 'category': BookCategory.CONTEMPORARY, 'drive_link': 'https://drive.google.com/file/d/book37', 'description': 'Lessons from the life of Muhammad for contemporary Muslims.'},
            {'title': 'Being Muslim', 'author': 'Haroon Moghul', 'category': BookCategory.CONTEMPORARY, 'drive_link': 'https://drive.google.com/file/d/book38', 'description': 'Finding meaning and purpose in the modern world as a Muslim.'},
            {'title': 'The Study Quran', 'author': 'Seyyed Hossein Nasr', 'category': BookCategory.CONTEMPORARY, 'drive_link': 'https://drive.google.com/file/d/book39', 'description': 'A new translation and commentary drawing on classical and modern scholarship.'},
            {'title': 'The Book of Islamic Dynasties', 'author': 'Luqman Nagy', 'category': BookCategory.CONTEMPORARY, 'drive_link': 'https://drive.google.com/file/d/book40', 'description': 'A celebration of Islamic history and civilization across centuries.'},
            {'title': 'Islam Between East and West', 'author': 'Alija Izetbegovic', 'category': BookCategory.CONTEMPORARY, 'drive_link': 'https://drive.google.com/file/d/book41', 'description': 'Philosophical analysis of Islam position in world civilizations.'},
            {'title': 'The Autobiography of Malcolm X', 'author': 'Malcolm X & Alex Haley', 'category': BookCategory.CONTEMPORARY, 'drive_link': 'https://drive.google.com/file/d/book42', 'description': 'Life story of the iconic Muslim leader and his journey to Islam.'},
            {'title': 'Destiny Disrupted', 'author': 'Tamim Ansary', 'category': BookCategory.CONTEMPORARY, 'drive_link': 'https://drive.google.com/file/d/book43', 'description': 'A history of the world through Islamic eyes.'},
            {'title': 'The Quran: A Biography', 'author': 'Bruce Lawrence', 'category': BookCategory.CONTEMPORARY, 'drive_link': 'https://drive.google.com/file/d/book44', 'description': 'The story of how the Quran came to be and its impact on history.'},
            {'title': 'American Islamic Fiction', 'author': 'G. Willow Wilson', 'category': BookCategory.CONTEMPORARY, 'drive_link': 'https://drive.google.com/file/d/book45', 'description': 'Collection of contemporary Muslim American literature.'},
            {'title': 'Misquoting Muhammad', 'author': 'Jonathan A.C. Brown', 'category': BookCategory.CONTEMPORARY, 'drive_link': 'https://drive.google.com/file/d/book46', 'description': 'The challenge and choices of interpreting the Prophets legacy.'},
            {'title': 'Longing for the Divine', 'author': 'Imam Zaid Shakir', 'category': BookCategory.CONTEMPORARY, 'drive_link': 'https://drive.google.com/file/d/book47', 'description': 'Spiritual reflections on faith, love, and seeking Allah.'},
            {'title': 'Journey to the Lord of Power', 'author': 'Ibn Arabi', 'category': BookCategory.CONTEMPORARY, 'drive_link': 'https://drive.google.com/file/d/book48', 'description': 'A Sufi manual on spiritual retreat and inner development.'},
            {'title': 'The Conference of the Birds', 'author': 'Farid ud-Din Attar', 'category': BookCategory.CONTEMPORARY, 'drive_link': 'https://drive.google.com/file/d/book49', 'description': 'Classic Sufi allegory about the spiritual journey to truth.'},
            {'title': 'Muslim Girl: A Coming of Age Story', 'author': 'Amani Al-Khatahtbeh', 'category': BookCategory.CONTEMPORARY, 'drive_link': 'https://drive.google.com/file/d/book50', 'description': 'Memoir about growing up Muslim American in post-9/11 world.'},
        ]

        for book_data in books:
            Book.objects.update_or_create(
                title=book_data['title'],
                defaults=book_data
            )
        self.stdout.write(f'  ✓ {len(books)} books created')

    def seed_events(self):
        """Create 50 events with mix of upcoming and past."""
        now = timezone.now()
        events_data = [
            # Upcoming events (20)
            {'title': 'Annual Youth Conference 2026', 'description': 'Join us for the biggest youth gathering of the year! Keynote speakers, panel discussions, workshops, and networking. Theme: "Youth Leading Change". Registration fee: ₹200', 'event_date': now + timedelta(days=30), 'location': 'Community Convention Center, RT Nagar', 'event_type': EventType.UPCOMING},
            {'title': 'Quran Competition 2026', 'description': 'Annual Quran recitation competition open to students aged 10-25. Categories: Hifz (5 Juz), Tilawat, and Tafseer Quiz. Prizes worth ₹50,000!', 'event_date': now + timedelta(days=45), 'location': 'Masjid-e-Noor, RT Nagar', 'event_type': EventType.UPCOMING},
            {'title': 'Career Fair 2026', 'description': 'Explore career opportunities with leading companies. Resume building workshop, mock interviews, and career counseling included.', 'event_date': now + timedelta(days=60), 'location': 'RT Nagar Community Hall', 'event_type': EventType.UPCOMING},
            {'title': 'Islamic Art Exhibition', 'description': 'Exhibition featuring calligraphy, geometric art, and Islamic architecture. Artists from across Karnataka participating.', 'event_date': now + timedelta(days=15), 'location': 'Art Gallery, RT Nagar', 'event_type': EventType.UPCOMING},
            {'title': 'Youth Leadership Summit', 'description': 'Two-day summit on developing leadership skills. Sessions by renowned speakers. Certificates and networking.', 'event_date': now + timedelta(days=20), 'location': 'Hotel Grand, RT Nagar', 'event_type': EventType.UPCOMING},
            {'title': 'Eid ul Adha Celebration 2026', 'description': 'Community Eid prayers followed by qurbani distribution. Family-friendly celebration with activities for children.', 'event_date': now + timedelta(days=75), 'location': 'Eidgah Ground, RT Nagar', 'event_type': EventType.UPCOMING},
            {'title': 'Sports Tournament 2026', 'description': 'Inter-community sports tournament featuring cricket, football, and badminton. Open registration for teams.', 'event_date': now + timedelta(days=35), 'location': 'Sports Complex, RT Nagar', 'event_type': EventType.UPCOMING},
            {'title': 'Book Fair 2026', 'description': 'Annual Islamic book fair with 20+ publishers. Special discounts and author meet sessions.', 'event_date': now + timedelta(days=25), 'location': 'Exhibition Hall, RT Nagar', 'event_type': EventType.UPCOMING},
            {'title': 'Health Camp', 'description': 'Free comprehensive health checkup camp. Eye, dental, and general health screenings available.', 'event_date': now + timedelta(days=10), 'location': 'SIO Office, RT Nagar', 'event_type': EventType.UPCOMING},
            {'title': 'Arabic Course Graduation', 'description': 'Graduation ceremony for Arabic course batch. Certificates distribution and student performances.', 'event_date': now + timedelta(days=40), 'location': 'Community Hall, RT Nagar', 'event_type': EventType.UPCOMING},
            {'title': 'Women Empowerment Conference', 'description': 'Conference addressing women issues in Islam. Panel discussions with female scholars.', 'event_date': now + timedelta(days=50), 'location': 'Ladies Hall, RT Nagar', 'event_type': EventType.UPCOMING},
            {'title': 'Tech Workshop for Students', 'description': 'Workshop on AI and Web Development. Hands-on sessions for college students.', 'event_date': now + timedelta(days=18), 'location': 'Computer Lab, RT Nagar', 'event_type': EventType.UPCOMING},
            {'title': 'Community Iftar Planning Meet', 'description': 'Planning meeting for upcoming Ramadan community iftar programs. Volunteers welcome.', 'event_date': now + timedelta(days=5), 'location': 'SIO Office, RT Nagar', 'event_type': EventType.UPCOMING},
            {'title': 'Inter-School Debate Competition', 'description': 'Debate competition on contemporary issues. Schools from RT Nagar area participating.', 'event_date': now + timedelta(days=22), 'location': 'School Auditorium, RT Nagar', 'event_type': EventType.UPCOMING},
            {'title': 'Nasheed Night', 'description': 'Evening of nasheeds and Islamic poetry. Local and guest nasheed artists performing.', 'event_date': now + timedelta(days=12), 'location': 'Open Air Theater, RT Nagar', 'event_type': EventType.UPCOMING},
            {'title': 'Dawah Training Workshop', 'description': 'Training on effective communication and presenting Islam. Role plays and practical exercises.', 'event_date': now + timedelta(days=28), 'location': 'Training Center, RT Nagar', 'event_type': EventType.UPCOMING},
            {'title': 'Photography Contest', 'description': 'Theme: "Islam in Daily Life". Open to all amateur photographers. Prizes worth ₹25,000.', 'event_date': now + timedelta(days=55), 'location': 'Online Submission', 'event_type': EventType.UPCOMING},
            {'title': 'Family Fun Day', 'description': 'Day out for SIO families with games, food, and activities. Kids special attractions.', 'event_date': now + timedelta(days=65), 'location': 'Park, RT Nagar', 'event_type': EventType.UPCOMING},
            {'title': 'Scholarship Distribution', 'description': 'Annual scholarship distribution for meritorious students from economically weak backgrounds.', 'event_date': now + timedelta(days=70), 'location': 'Town Hall, RT Nagar', 'event_type': EventType.UPCOMING},
            {'title': 'New Year Islamic Program', 'description': 'Welcome the new Islamic year with special prayers, lectures, and community dinner.', 'event_date': now + timedelta(days=80), 'location': 'Masjid, RT Nagar', 'event_type': EventType.UPCOMING},
            
            # Past events (30)
            {'title': 'Ramadan Awareness Program 2026', 'description': 'Special program during Ramadan focusing on spiritual significance. Daily lectures and community iftars. Over 500 participants.', 'event_date': now - timedelta(days=60), 'location': 'Various locations in RT Nagar', 'event_type': EventType.PAST},
            {'title': 'Blood Donation Camp March 2026', 'description': 'Collected 150+ units of blood in collaboration with Red Cross. All donors received health certificates.', 'event_date': now - timedelta(days=90), 'location': 'Government Hospital, RT Nagar', 'event_type': EventType.PAST},
            {'title': 'Educational Excellence Awards 2025', 'description': 'Annual ceremony recognizing 50 academic achievers. Chief Guest: Dr. Abdul Kareem, Vice Chancellor.', 'event_date': now - timedelta(days=180), 'location': 'Town Hall, RT Nagar', 'event_type': EventType.PAST},
            {'title': 'Winter Relief Distribution', 'description': 'Distributed blankets and warm clothes to 300 families in slum areas.', 'event_date': now - timedelta(days=150), 'location': 'Community Center, RT Nagar', 'event_type': EventType.PAST},
            {'title': 'Republic Day Celebration', 'description': 'Flag hoisting and cultural program celebrating national unity and constitutional values.', 'event_date': now - timedelta(days=155), 'location': 'School Ground, RT Nagar', 'event_type': EventType.PAST},
            {'title': 'Annual Sports Day 2025', 'description': 'Full day of sports competitions. Cricket, football, and athletics. 200+ participants.', 'event_date': now - timedelta(days=200), 'location': 'Sports Ground, RT Nagar', 'event_type': EventType.PAST},
            {'title': 'Eid ul Fitr Celebration 2026', 'description': 'Grand Eid celebration with prayers, community breakfast, and gift distribution to children.', 'event_date': now - timedelta(days=45), 'location': 'Eidgah, RT Nagar', 'event_type': EventType.PAST},
            {'title': 'Environment Day Tree Plantation', 'description': 'Planted 100 trees across RT Nagar in collaboration with Forest Department.', 'event_date': now - timedelta(days=25), 'location': 'Various Parks, RT Nagar', 'event_type': EventType.PAST},
            {'title': 'Youth Poetry Competition', 'description': 'Urdu and English poetry competition on Islamic themes. 40 participants from colleges.', 'event_date': now - timedelta(days=70), 'location': 'Auditorium, RT Nagar', 'event_type': EventType.PAST},
            {'title': 'Career Guidance Seminar', 'description': 'Seminar on engineering and medical career options. 150 students attended.', 'event_date': now - timedelta(days=85), 'location': 'College Hall, RT Nagar', 'event_type': EventType.PAST},
            {'title': 'Iftar Meet with Orphans', 'description': 'Special iftar organized for orphan children. Fun activities and gifts distributed.', 'event_date': now - timedelta(days=50), 'location': 'Orphanage, RT Nagar', 'event_type': EventType.PAST},
            {'title': 'Community Cleaning Drive', 'description': 'Cleaned up main market area and planted flowering plants. 80 volunteers participated.', 'event_date': now - timedelta(days=100), 'location': 'Main Market, RT Nagar', 'event_type': EventType.PAST},
            {'title': 'Islamic Finance Workshop', 'description': 'Workshop on halal investments and Islamic banking. Expert from Islamic bank conducted.', 'event_date': now - timedelta(days=110), 'location': 'Conference Room, RT Nagar', 'event_type': EventType.PAST},
            {'title': 'Quiz Competition 2025', 'description': 'General knowledge and Islamic quiz. 25 teams participated. Exciting finals.', 'event_date': now - timedelta(days=220), 'location': 'School Hall, RT Nagar', 'event_type': EventType.PAST},
            {'title': 'Annual Day Celebration 2025', 'description': 'Foundation day celebration with cultural program and chief guest address.', 'event_date': now - timedelta(days=365), 'location': 'Community Hall, RT Nagar', 'event_type': EventType.PAST},
            {'title': 'Mothers Day Special Program', 'description': 'Program honoring mothers with gifts and appreciation certificates.', 'event_date': now - timedelta(days=130), 'location': 'Ladies Hall, RT Nagar', 'event_type': EventType.PAST},
            {'title': 'Youth Picnic 2026', 'description': 'Recreational picnic to Nandi Hills. Team building activities and games.', 'event_date': now - timedelta(days=35), 'location': 'Nandi Hills', 'event_type': EventType.PAST},
            {'title': 'Job Fair 2025', 'description': 'Job fair with 15 companies. 200+ students attended. Many received offer letters.', 'event_date': now - timedelta(days=240), 'location': 'Convention Center, RT Nagar', 'event_type': EventType.PAST},
            {'title': 'Quran Khatam Program', 'description': 'Special program completing collective Quran reading during Ramadan.', 'event_date': now - timedelta(days=55), 'location': 'Masjid, RT Nagar', 'event_type': EventType.PAST},
            {'title': 'Independence Day Flag Hoisting', 'description': 'Patriotic program with flag hoisting, speeches and cultural activities.', 'event_date': now - timedelta(days=320), 'location': 'School Ground, RT Nagar', 'event_type': EventType.PAST},
            {'title': 'Eid Milad Un Nabi 2025', 'description': 'Celebration of Prophets birthday with nasheeds, lectures and community feast.', 'event_date': now - timedelta(days=280), 'location': 'Masjid, RT Nagar', 'event_type': EventType.PAST},
            {'title': 'Blood Donation Camp Sept 2025', 'description': 'Quarterly blood donation drive. 100 units collected.', 'event_date': now - timedelta(days=300), 'location': 'Hospital, RT Nagar', 'event_type': EventType.PAST},
            {'title': 'Summer Camp Valedictory', 'description': 'Closing ceremony of 2-week summer camp. Talent show by children.', 'event_date': now - timedelta(days=380), 'location': 'School, RT Nagar', 'event_type': EventType.PAST},
            {'title': 'Teachers Day Program', 'description': 'Honoring teachers with felicitation and gifts. Students performances.', 'event_date': now - timedelta(days=295), 'location': 'School Auditorium, RT Nagar', 'event_type': EventType.PAST},
            {'title': 'Diwali Sweets Distribution', 'description': 'Distributed sweets to neighbors promoting communal harmony.', 'event_date': now - timedelta(days=250), 'location': 'Various Areas, RT Nagar', 'event_type': EventType.PAST},
            {'title': 'New Member Welcome Program', 'description': 'Orientation for 30 new members. Explained SIO mission and activities.', 'event_date': now - timedelta(days=120), 'location': 'SIO Office, RT Nagar', 'event_type': EventType.PAST},
            {'title': 'Film Screening - The Message', 'description': 'Screened historical movie on early Islam. Discussion session followed.', 'event_date': now - timedelta(days=140), 'location': 'Mini Theater, RT Nagar', 'event_type': EventType.PAST},
            {'title': 'Cyber Safety Awareness', 'description': 'Session on internet safety for students. Expert from cyber cell addressed.', 'event_date': now - timedelta(days=160), 'location': 'College, RT Nagar', 'event_type': EventType.PAST},
            {'title': 'Old Age Home Visit', 'description': 'Spent quality time with elderly. Distributed fruits and essentials.', 'event_date': now - timedelta(days=175), 'location': 'Old Age Home, RT Nagar', 'event_type': EventType.PAST},
            {'title': 'Urs Sharif Participation', 'description': 'Participated in local Sufi saint annual gathering promoting interfaith harmony.', 'event_date': now - timedelta(days=190), 'location': 'Dargah, RT Nagar', 'event_type': EventType.PAST},
        ]

        for event_data in events_data:
            Event.objects.update_or_create(
                title=event_data['title'],
                defaults=event_data
            )
        self.stdout.write(f'  ✓ {len(events_data)} events created')

    def seed_announcements(self):
        """Create 50 announcements with mix of pinned and regular."""
        announcements = [
            # Pinned announcements (5)
            {'title': '🎉 Registration Open for Annual Youth Conference 2026', 'content': 'We are excited to announce that registrations are now open for our Annual Youth Conference 2026!\n\nTheme: "Youth Leading Change"\nDate: July 28, 2026\nVenue: Community Convention Center, RT Nagar\n\nEarly bird discount: 20% off until July 10, 2026\nRegister now at: https://siortnagar.org/register', 'is_pinned': True},
            {'title': '📚 50 New Books Added to Digital Library', 'content': 'We have added 50 new books to our digital library! Check out the latest additions including works by renowned Islamic scholars and contemporary Muslim authors.\n\nAll books are available for free download for our registered members. Visit the Library section to explore.\n\nHappy reading!', 'is_pinned': True},
            {'title': '🏆 Scholarship Applications Now Open', 'content': 'SIO RT Nagar announces scholarship program for academically bright students from economically weak backgrounds.\n\nEligibility: Students scoring above 80% in board exams\nAmount: Up to ₹25,000 per year\nDeadline: July 31, 2026\n\nApply online at our website.', 'is_pinned': True},
            {'title': '🤝 Volunteer Recruitment Drive', 'content': 'SIO RT Nagar is looking for dedicated volunteers!\n\nAreas we need help:\n- Event management\n- Social media handling\n- Teaching and mentoring\n- Community outreach\n\nFill out the volunteer form on our website.', 'is_pinned': True},
            {'title': '📢 New Office Location Announcement', 'content': 'We have moved to a new, larger office space!\n\nNew Address:\n123, 2nd Cross, RT Nagar Main Road\nNear City Mall, RT Nagar\nBangalore - 560032\n\nAll are welcome to visit us!', 'is_pinned': True},
            
            # Regular announcements (45)
            {'title': 'Weekly Study Circle - Schedule Update', 'content': 'Our weekly Quran Study Circle has been rescheduled from Saturday to Sunday.\n\nNew timing: Every Sunday, 10:00 AM - 12:00 PM\nVenue: SIO Office, RT Nagar\n\nContact education secretary for queries.', 'is_pinned': False},
            {'title': 'Thank You - Blood Donation Camp Success', 'content': 'Alhamdulillah! Our blood donation camp collected over 150 units of blood!\n\nSpecial thanks to:\n- Red Cross Society\n- All generous donors\n- Volunteer team\n- Hospital staff', 'is_pinned': False},
            {'title': 'Office Timings During Summer', 'content': 'Summer office timings:\nMonday to Friday: 5:00 PM - 8:00 PM\nSaturday: 10:00 AM - 1:00 PM\nSunday: Closed\n\nRegular timings resume July 15, 2026.', 'is_pinned': False},
            {'title': 'Arabic Course - New Batch Starting', 'content': 'New batch for Arabic language course starting soon!\n\nDuration: 3 months\nTiming: Weekends\nFee: ₹1,500 only\n\nRegistration open at office.', 'is_pinned': False},
            {'title': 'Congratulations to Board Exam Toppers', 'content': 'Heartiest congratulations to all SIO students who excelled in board exams!\n\nSpecial mention: Ahmed scored 98% in SSLC, Fatima scored 96% in PUC.\n\nProud of our students!', 'is_pinned': False},
            {'title': 'Community Iftar - Sponsors Needed', 'content': 'We are organizing community iftar during Ramadan.\n\nSponsor one day iftar: ₹5,000\nSponsors will be recognized during the program.\n\nContact Treasurer for details.', 'is_pinned': False},
            {'title': 'Sports Tournament Registration Open', 'content': 'Register your team for upcoming sports tournament!\n\nSports: Cricket, Football, Badminton\nTeam Size: As per sport rules\nEntry Fee: ₹500 per team\n\nLast date: Next Friday', 'is_pinned': False},
            {'title': 'Career Counseling Sessions Available', 'content': 'Free career counseling sessions for students!\n\nEvery Wednesday: 4:00 PM - 6:00 PM\nPre-registration required\n\nBook your slot via WhatsApp.', 'is_pinned': False},
            {'title': 'Library Hours Extended', 'content': 'Good news! Library hours extended due to exam season.\n\nNew Timing: 9:00 AM - 9:00 PM (All days)\n\nValid till exams end. Utilize the quiet space!', 'is_pinned': False},
            {'title': 'Eid Gifts Collection Drive', 'content': 'Collecting Eid gifts for orphan children!\n\nAccepted items: New clothes, toys, chocolates, stationery\nDrop-off: SIO Office\n\nDeadline: One week before Eid', 'is_pinned': False},
            {'title': 'Photography Contest Results', 'content': 'Photography contest results announced!\n\n1st Prize: Mohammad Ali\n2nd Prize: Aisha Khan\n3rd Prize: Yusuf Ahmed\n\nCongratulations to all winners!', 'is_pinned': False},
            {'title': 'Monthly Meeting - All Members', 'content': 'Monthly members meeting scheduled.\n\nDate: First Sunday of every month\nTime: 11:00 AM\nVenue: SIO Office\n\nAttendance is mandatory for active members.', 'is_pinned': False},
            {'title': 'Tree Plantation Drive - Volunteers Needed', 'content': 'Join us for tree plantation drive on Environment Day!\n\nDate: June 5, 2026\nMeeting Point: SIO Office, 7:00 AM\n\nBring gardening gloves if you have.', 'is_pinned': False},
            {'title': 'Nasheed Workshop Registration', 'content': 'Learn nasheeds from professional artists!\n\n3-day workshop\nFee: ₹300\nCertificates provided\n\nLimited seats. Register now!', 'is_pinned': False},
            {'title': 'Zakat Collection and Distribution', 'content': 'SIO facilitates Zakat collection and distribution.\n\nTrusted and transparent process\nReceipts provided\nDistributed to eligible recipients locally\n\nContact office for details.', 'is_pinned': False},
            {'title': 'Guest Lecture by Dr. Zakir Naik', 'content': 'Special announcement! Online lecture by Dr. Zakir Naik.\n\nTopic: "Islam and Modern Science"\nDate: Check website\nLink: Will be shared on social media', 'is_pinned': False},
            {'title': 'First Aid Training - Free', 'content': 'Free first aid training in collaboration with Red Cross!\n\nDate: Coming Saturday\nTime: 10:00 AM - 4:00 PM\nCertificates provided\n\nRegister at office.', 'is_pinned': False},
            {'title': 'Book Review Session', 'content': 'Join our book review session!\n\nBook: "Towards Understanding Islam"\nPresenter: Br. Abdullah\nDate: Next Sunday after Zuhr\n\nAll are welcome.', 'is_pinned': False},
            {'title': 'Women Circle - New Timings', 'content': 'Women study circle new schedule:\n\nEvery Friday: 11:00 AM - 1:00 PM\nVenue: Ladies Section, SIO Office\n\nChildcare facility available.', 'is_pinned': False},
            {'title': 'Exam Prayer Session', 'content': 'Special dua session for students appearing in exams.\n\nDate: Before exam season\nTime: After Fajr\nVenue: Masjid\n\nParents can attend.', 'is_pinned': False},
            {'title': 'Website Launch Announcement', 'content': 'Our new website is now live!\n\nFeatures: Event registration, Digital library, News updates\nVisit: www.siortnagar.org\n\nFeedback welcome!', 'is_pinned': False},
            {'title': 'Ramadan Timetable Available', 'content': 'Ramadan timetable with Sehri/Iftar times available!\n\nDownload from website or collect printed copy from office.\n\nRamadan Mubarak in advance!', 'is_pinned': False},
            {'title': 'Marriage Bureau Service', 'content': 'SIO offers free marriage bureau service.\n\nRegistration: Office or online\nConfidential process\nMatches within community\n\nContact for details.', 'is_pinned': False},
            {'title': 'Orphan Sponsorship Program', 'content': 'Sponsor an orphan education!\n\nMonthly sponsorship: ₹1,500\nCovers: School fees, books, uniform\n\nChange a life today. Contact us.', 'is_pinned': False},
            {'title': 'Quiz Competition - Register Now', 'content': 'Inter-school Islamic quiz competition!\n\nTeam size: 3 members\nPrizes worth ₹30,000\nRegistration fee: ₹100 per team\n\nLast date approaching!', 'is_pinned': False},
            {'title': 'Eid Namaz Timing', 'content': 'Eid ul Fitr namaz timings:\n\n1st Jamaat: 7:00 AM\n2nd Jamaat: 8:00 AM\n3rd Jamaat: 9:00 AM\n\nVenue: Eidgah Ground', 'is_pinned': False},
            {'title': 'Flood Relief Collection', 'content': 'Collecting materials for flood-affected areas.\n\nNeeded: Clothes, food items, medicines\nDrop: SIO Office\n\nHelp our brothers and sisters in need.', 'is_pinned': False},
            {'title': 'Computer Classes for Seniors', 'content': 'Basic computer classes for senior citizens!\n\nFree of cost\nWeekends only\nPersonal attention\n\nBring your parents/grandparents!', 'is_pinned': False},
            {'title': 'Inter-College Debate Results', 'content': 'Debate competition results:\n\nWinner: ABC College\nRunner-up: XYZ College\nBest Speaker: Mariam from ABC College\n\nCongratulations!', 'is_pinned': False},
            {'title': 'Taraweeh Arrangement', 'content': 'Taraweeh prayers will be held at:\n\nMasjid-e-Noor: Full Quran recitation\nCommunity Hall: Short Taraweeh\n\nAll welcome.', 'is_pinned': False},
            {'title': 'Youth Camp - Limited Seats', 'content': '3-day youth camp announcement!\n\nActivities: Trekking, team building, Islamic sessions\nFee: ₹2,000 (includes food, stay, transport)\n\nHurry! Limited seats.', 'is_pinned': False},
            {'title': 'Feedback Form for Programs', 'content': 'Your feedback matters!\n\nPlease fill the feedback form after attending any program.\nLink available on website.\n\nHelp us improve!', 'is_pinned': False},
            {'title': 'New Members Welcome', 'content': 'Welcome to all new SIO members who joined this month!\n\nOrientation session scheduled for next Sunday.\n\nLooking forward to working together.', 'is_pinned': False},
            {'title': 'Health Insurance Scheme', 'content': 'Group health insurance for SIO members!\n\nAffordable premium\nFamily coverage\nNetwork hospitals\n\nEnquire at office.', 'is_pinned': False},
            {'title': 'Tahajjud Camp Registration', 'content': 'Special Tahajjud camp during last 10 days of Ramadan.\n\nStay overnight at masjid\nQuran recitation and dua\n\nRegister with caretaker.', 'is_pinned': False},
            {'title': 'Interview Preparation Workshop', 'content': 'Job interview preparation workshop!\n\nMock interviews\nResume review\nDress code guidance\n\nFor final year students. Free!', 'is_pinned': False},
            {'title': 'Sadaqah Collection Drive', 'content': 'Regular Sadaqah collection for community welfare.\n\nMonthly contribution option available.\nAll funds used locally.\n\nContact Treasurer.', 'is_pinned': False},
            {'title': 'Islamic Calligraphy Classes', 'content': 'Learn beautiful Arabic calligraphy!\n\n10-session course\nMaterials provided\nFee: ₹500\n\nDisplay your artwork at exhibition!', 'is_pinned': False},
            {'title': 'Parents Meeting Invitation', 'content': 'Parents are invited for quarterly meeting.\n\nAgenda: Student progress, upcoming programs, suggestions\nDate: Last Sunday of month\nTime: 5:00 PM', 'is_pinned': False},
            {'title': 'Eid Mubarak to All!', 'content': 'SIO RT Nagar wishes everyone Eid Mubarak!\n\nMay Allah accept our prayers and fasting.\nMay this Eid bring joy and blessings to all.\n\nTaqabbal Allahu minna wa minkum!', 'is_pinned': False},
            {'title': 'Office Closed - Public Holiday', 'content': 'SIO Office will remain closed on [date] due to public holiday.\n\nFor emergencies, contact General Secretary.\n\nResume normal timings next day.', 'is_pinned': False},
            {'title': 'Social Media Contest', 'content': 'Share your favorite SIO memory on social media!\n\nUse hashtag #SIOrtnagar\nBest posts win prizes\n\nContest ends this month.', 'is_pinned': False},
            {'title': 'Senior Members Felicitation', 'content': 'Special program to honor founding and senior members.\n\nDate: Foundation Day\nVenue: Community Hall\n\nAll members invited.', 'is_pinned': False},
            {'title': 'Hifz Competition Announcement', 'content': 'Annual Hifz competition for children!\n\nCategories: 5 Surah, 10 Surah, 1 Juz\nPrizes for all participants\n\nRegister your child now.', 'is_pinned': False},
        ]

        for announcement_data in announcements:
            Announcement.objects.update_or_create(
                title=announcement_data['title'],
                defaults=announcement_data
            )
        self.stdout.write(f'  ✓ {len(announcements)} announcements created')

    def seed_contact_info(self):
        """Create contact information."""
        ContactInfo.objects.update_or_create(
            is_active=True,
            defaults={
                'office_address': '''SIO RT Nagar Chapter
123, 2nd Cross, RT Nagar Main Road,
Near City Mall, RT Nagar,
Bangalore - 560032
Karnataka, India''',
                'google_maps_embed_url': 'https://maps.google.com/maps?q=RT+Nagar+Bangalore&output=embed',
                'phone_numbers': ['+91 9876543210', '+91 9876543212', '+91 80-12345678'],
                'email': 'contact@siortnagar.org',
                'social_media_links': {
                    'facebook': 'https://facebook.com/siortnagar',
                    'instagram': 'https://instagram.com/siortnagar',
                    'twitter': 'https://twitter.com/siortnagar',
                    'youtube': 'https://youtube.com/@siortnagar',
                    'whatsapp': 'https://wa.me/919876543210',
                },
                'google_form_link': 'https://forms.gle/abc123xyz',
            }
        )
        self.stdout.write('  ✓ Contact info created')
