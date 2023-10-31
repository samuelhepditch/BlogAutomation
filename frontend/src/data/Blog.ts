import { BlogStatus } from "./BlogStatus";

class Blog {
    index: number;
    topic: string;
    keywords: string;
    status: BlogStatus;
    notes: string;

    constructor(index: number, topic: string, keywords: string, status: BlogStatus) {
        this.index = index;
        this.topic = topic;
        this.keywords = keywords;
        this.status = status;
        this.notes = "";
    }
}

export default Blog;