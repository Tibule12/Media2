import { describe, it, expect } from 'vitest';
import { mount } from '@vue/test-utils';
import StoryCreate from '../StoryCreate.vue';

describe('StoryCreate.vue', () => {
  it('renders story create form', () => {
    const wrapper = mount(StoryCreate);
    expect(wrapper.exists()).toBe(true);
  });
});
