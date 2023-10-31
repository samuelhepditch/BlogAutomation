class Blog {
    topic: string;
    keywords: string;
    status: 'in progress' | 'failed' | 'successful';

    constructor(topic: string, keywords: string, status: 'in progress' | 'failed' | 'successful') {
        this.topic = topic;
        this.keywords = keywords;
        this.status = status;
    }
}

export default Blog;