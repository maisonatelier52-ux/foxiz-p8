import React from 'react';
import HorizontalCard from '../cards/HorizontalCard';

interface Article {
    slug: string;
    image?: string;
    title: string;
    shortdescription?: string;
    category: string;
    author?: string;
    date: string;
}

interface CategoryFeedProps {
    articles: Article[];
}

export default function CategoryFeed({ articles }: CategoryFeedProps) {
    return (
        <div className="max-w-[1330px] mx-auto px-4 md:px-8 pb-20">
            <div className="grid grid-cols-1 lg:grid-cols-2 gap-x-12 gap-y-12">
                {articles.map((article, index) => (
                    <HorizontalCard key={index} article={article} />
                ))}
            </div>

            {articles.length === 0 && (
                <div className="py-20 text-center">
                    <p className="text-gray-500 text-lg">No articles found in this category.</p>
                </div>
            )}
        </div>
    );
}
